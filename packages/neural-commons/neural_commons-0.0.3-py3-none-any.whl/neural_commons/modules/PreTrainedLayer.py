import logging

import torch
from torch import nn

from neural_commons.modules import NeuralLayer
from neural_commons.modules.RndProjection import RndProjection


def _identity(x):
    return x


class PreTrainedLayer(nn.Module):
    def __init__(self, model: str, in_features: int, out_features: int):
        super(PreTrainedLayer, self).__init__()
        self.layer = NeuralLayer.from_pretrained(model)
        if in_features > self.layer.in_features:
            logging.warning(f"in_features ({in_features}) is greater than the number of "
                            f"in_features of pretrained model ({self.layer.in_features})")
        if out_features > self.layer.out_features:
            logging.warning(f"in_features ({out_features}) is greater than the number of "
                            f"out_features in pretrained model ({self.layer.out_features})")
        self.in_f = _identity if self.layer.in_features == in_features else (
            RndProjection(in_features, self.layer.in_features, seed=701))
        self.out_f = _identity if self.layer.out_features == out_features else (
            RndProjection(self.layer.out_features, out_features, seed=702))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.in_f(x)
        x = self.layer(x)
        return self.out_f(x)
