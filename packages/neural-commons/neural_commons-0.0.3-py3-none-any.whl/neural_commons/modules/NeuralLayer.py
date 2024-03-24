import dataclasses
import math
from dataclasses import dataclass

import torch
from huggingface_hub import PyTorchModelHubMixin
from torch import nn, Tensor
from torch.nn import Parameter, init
import torch.nn.functional as F


def get_torch_dtype(dtype_str):
    if hasattr(torch, dtype_str):
        return getattr(torch, dtype_str)
    else:
        raise ValueError(f"Unknown dtype string: {dtype_str}")


@dataclass
class NeuralLayerConfig:
    in_features: int
    out_features: int
    bias: bool = True
    dtype: str = "float32"


class NeuralLayer(nn.Module, PyTorchModelHubMixin):
    __constants__ = ['in_features', 'out_features']
    in_features: int
    out_features: int
    weight: Tensor
    hp_params: Tensor

    def __init__(self, config: NeuralLayerConfig) -> None:
        if isinstance(config, dict):
            config = NeuralLayerConfig(**config)
        super().__init__()
        dtype = get_torch_dtype(config.dtype)
        self.config = config
        self.convert_input = dtype != torch.float and dtype != torch.float32
        self.in_features = config.in_features
        self.out_features = config.out_features
        self.slopes = nn.Parameter(torch.ones(self.out_features, dtype=dtype))
        setattr(self.slopes, "__skip_transplant__", True)
        self.weight = Parameter(torch.empty((self.out_features, self.in_features,), dtype=dtype))
        if config.bias:
            self.bias = Parameter(torch.empty(self.out_features, dtype=dtype))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    @classmethod
    def build(cls, in_features: int, out_features: int, bias: bool = True,
              dtype: str = "float32"):
        return cls(NeuralLayerConfig(in_features=in_features,
                                     out_features=out_features,
                                     bias=bias, dtype=dtype))

    def reset_parameters(self) -> None:
        # Setting a=sqrt(5) in kaiming_uniform is the same as initializing with
        # uniform(-1/sqrt(in_features), 1/sqrt(in_features)). For details, see
        # https://github.com/pytorch/pytorch/issues/57109
        init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in, _ = init._calculate_fan_in_and_fan_out(self.weight)
            bound = 1 / math.sqrt(fan_in) if fan_in > 0 else 0
            init.uniform_(self.bias, -bound, bound)

    def forward(self, x: Tensor) -> Tensor:
        x = F.linear(x, self.weight, self.bias)
        positive = x >= 0
        return positive * x + (~positive) * x * self.slopes[None, :]

    def extra_repr(self) -> str:
        return f'in_features={self.in_features}, out_features={self.out_features}, bias={self.bias is not None}'


