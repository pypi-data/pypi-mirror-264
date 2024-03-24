import math
from typing import Iterable, Optional
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F

_sqrt_2 = math.sqrt(2)


def count_parameters(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)


def count_parameters_from_list(param_list: Iterable[nn.Parameter]):
    return sum(p.numel() for p in param_list)


def sin_pos_embeddings(seq_len: int, emb_dim: int) -> torch.Tensor:
    factors = torch.arange(1, emb_dim + 1)
    seq_range = torch.arange(0, seq_len)
    angles = math.pi * 2 * seq_range / seq_len
    return torch.sin(angles[:, None] * factors[None, :]) * _sqrt_2


def concatenate_tensors(list_of_tensors):
    if isinstance(list_of_tensors[0], tuple):
        concatenated_tuples = []
        for i in range(len(list_of_tensors[0])):
            concatenated_tensors = torch.cat([t[i] for t in list_of_tensors], dim=0)
            concatenated_tuples.append(concatenated_tensors)
        return tuple(concatenated_tuples)
    else:
        return torch.cat(list_of_tensors, dim=0)


def batched_apply(model: nn.Module, x: torch.Tensor, batch_size: int = 64, detached: bool = False):
    output_list = []
    num_items = x.size(0)
    for b0 in range(0, num_items, batch_size):
        input_batch = x[b0:b0 + batch_size]
        output_batch = model(input_batch)
        if detached:
            if isinstance(output_batch, tuple):
                output_batch = tuple([x.detach() for x in output_batch])
            else:
                output_batch = output_batch.detach()
        output_list.append(output_batch)
    output = concatenate_tensors(output_list)
    return output


def sample_tensor(tensor: torch.Tensor, count: int):
    perm = torch.randperm(tensor.size(0), device=tensor.device)
    return tensor[perm[:count]]


def sample_tensors(tensor1: torch.Tensor, tensor2: torch.Tensor, count: int):
    if tensor2.size(0) != tensor1.size(0):
        raise ValueError('Different batch sizes!')
    perm = torch.randperm(tensor1.size(0), device=tensor1.device)
    selection = perm[:count]
    return tensor1[selection], tensor2[selection],


def fixed_hash(text: str):
    h = 0
    for ch in text:
        h = (h * 281 ^ ord(ch) * 997) & 0xFFFFFFFF
    return h


def tensor_hash(t: torch.Tensor):
    return fixed_hash(str(t.cpu().tolist()))


def unfold_2d(tensor: torch.Tensor, patch_size: int, step_size: int):
    # tensor shape: (channels, height, width)
    # result shape: (num_patches, channels, patch_size, patch_size)
    _, orig_height, orig_width = tensor.shape
    if orig_width < patch_size or orig_height < patch_size:
        raise ValueError(f'Tensor too small for patch_size={patch_size}')
    num_rows = math.ceil((orig_height - patch_size) / step_size) + 1
    num_cols = math.ceil((orig_width - patch_size) / step_size) + 1
    num_patches = num_rows * num_cols
    new_height = (num_rows - 1) * step_size + patch_size
    new_width = (num_cols - 1) * step_size + patch_size
    if new_height != orig_height or new_width != orig_width:
        padding_height = new_height - orig_height
        padding_width = new_width - orig_width
        tensor = F.pad(tensor, pad=(0, padding_width, 0, padding_height))
    # tensor shape: (channels, height, width)
    patches = tensor.unfold(1, patch_size, step_size)
    patches = patches.unfold(2, patch_size, step_size)
    patches = patches.contiguous().view((3, num_patches, patch_size, patch_size))
    patches_input = torch.permute(patches, (1, 0, 2, 3))
    return patches_input


def fold_2d(tensor: torch.Tensor, width: int, height: int):
    # tensor shape: (num_patches, channels, patch_size, patch_size)
    # result shape: (channels, height, width)
    num_patches, channels, patch_size, _ = tensor.shape
    step_size = patch_size
    num_rows = math.ceil(height / step_size)
    num_cols = math.ceil(width / step_size)
    if num_patches != num_rows * num_cols:
        raise ValueError(f'Expected num_rows={num_rows} * num_cols={num_cols} to be {num_patches}')
    new_height = num_rows * patch_size
    new_width = num_cols * patch_size
    tensor = torch.permute(tensor, (1, 0, 2, 3))
    # tensor: (channels, num_patches, patch_size, patch_size)
    tensor = tensor.view(channels, num_rows, num_cols, patch_size, patch_size)
    tensor = torch.permute(tensor, (0, 1, 3, 2, 4))
    # tensor: (channels, num_rows, patch_size, num_cols, patch_size)
    tensor = tensor.contiguous().view(channels, new_height, new_width)
    return torch.clone(tensor[:, :height, :width])


def get_param_map(parameters: Iterable[nn.Parameter]):
    """
    Takes an iterable of PyTorch Parameters and creates a parameter map.

    Args:
        parameters (iterable): An iterable containing PyTorch nn.Parameter objects.

    Returns:
        dict: A dictionary with:
            * Keys: Dimension counts (1, 2, 3, etc.)
            * Values: Lists of tuples, each tuple containing:
                * The number of parameters in the tensor
                * The parameter tensor itself
    """

    param_map = {}
    for param in parameters:
        num_params = param.numel()
        dimension = len(param.size())

        if dimension not in param_map:
            param_map[dimension] = []
        param_map[dimension].append((num_params, param))

    return param_map


def extract_matching_param(param_map: dict[int, list],
                           expected_shape: tuple[int, ...],
                           ok_remove_all: bool = False) -> Optional[nn.Parameter]:
    """
    Extracts a parameter from a parameter map based on the best shape match, with
    priority on the closest number of parameters using binary search.

    Args:
        param_map (dict): A parameter map as returned by the 'get_param_map' function.
        expected_shape (tuple): The expected shape of the parameter tensor to extract.

    Returns:
        torch.nn.Parameter: The best matching parameter (if found), otherwise None.
        The parameter is also removed from the input 'param_map'.
    """

    dimension = len(expected_shape)
    if dimension not in param_map:
        return None  # No parameters with the specified dimension

    # Extract relevant list and focus on the number of parameters
    tuple_list = param_map[dimension]
    expected_shape_pt = torch.tensor(expected_shape)
    param_for_match = None
    index_for_match = -1
    min_dist = np.Inf
    for i, (_, param) in enumerate(tuple_list):
        shape = param.shape
        dist = torch.mean((torch.tensor(shape, dtype=torch.float) -
                           expected_shape_pt).pow(2)).item()
        if dist < min_dist:
            min_dist = dist
            param_for_match = param
            index_for_match = i
    if index_for_match >= 0 and (len(tuple_list) > 1 or ok_remove_all):
        del tuple_list[index_for_match]
    return param_for_match


def scale_nearest(tensor: torch.Tensor, expected_shape: tuple[int, ...]) -> torch.Tensor:
    shape = tensor.shape
    if len(shape) != len(expected_shape):
        raise ValueError("Number of tensor dimensions does not match dimensions of expected shape!")
    result = tensor
    for i, (d_size, exp_d_size) in enumerate(zip(shape, expected_shape)):
        if i != 0:
            t_result = torch.transpose(result, 0, i)
        else:
            t_result = result
        scale = d_size / exp_d_size
        indexes = (torch.arange(0, exp_d_size) * scale).long()
        t_result = t_result[indexes]
        if i != 0:
            result = torch.transpose(t_result, 0, i)
        else:
            result = t_result
    return result


def transplant_params(source_params: Iterable[nn.Parameter],
                      target_params: Iterable[nn.Parameter],
                      verbose=False):
    """
    Initializes target parameters with best matching parameters from source, scaling as needed.

    Args:
        source_params (Iterable[nn.Parameter]): Parameters from source model.
        target_params (Iterable[nn.Parameter]): Parameters to be initialized.
        verbose (bool): If True, prints information about the parameter transplant process.
    """
    with torch.no_grad():
        source_param_map = get_param_map(source_params)
        for target_param in target_params:
            expected_target_shape = target_param.shape
            dimension = len(expected_target_shape)
            if getattr(target_param, "__skip_transplant__", False):
                if verbose:
                    print(f"Warning: Skipping parameter tensor of {dimension} dimensions.")
                continue
            matched_param = extract_matching_param(source_param_map, expected_target_shape)
            if matched_param is None:
                if verbose:
                    print(f"Warning: No matching parameter found for target "
                          f"parameter with shape {expected_target_shape}")
                continue

            if verbose:
                print(f"Replacing target of shape {expected_target_shape} "
                      f"with source of shape {matched_param.shape}")

            if matched_param.shape != expected_target_shape:
                param_data = scale_nearest(matched_param.data, expected_target_shape)
            else:
                param_data = matched_param.data
            source_scale = torch.std(param_data).item()
            source_scale = max(source_scale, 1e-10)
            target_scale = torch.std(target_param.data).item()
            param_data = param_data * target_scale / source_scale
            param_data = param_data.detach()
            target_param.data.copy_(param_data)
