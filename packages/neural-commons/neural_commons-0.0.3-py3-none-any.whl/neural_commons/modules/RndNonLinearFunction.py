import torch
import torch.nn as nn

_act_fns = [
    nn.ReLU(),
    nn.GELU(),
    nn.ELU(),
    nn.SELU(),
]


class RndNonLinearFunction(nn.Module):
    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        hidden_size = max(input_size, output_size) * 15
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            self.rnd_activation_fn(),

            nn.Linear(hidden_size, hidden_size),
            self.rnd_activation_fn(),

            nn.Linear(hidden_size, hidden_size),
            self.rnd_activation_fn(),

            nn.Linear(hidden_size, output_size),
        )

    @staticmethod
    def rnd_activation_fn():
        choice = torch.randint(0, 4, size=(1,)).item()
        return _act_fns[choice]

    def forward(self, x):
        return self.layers(x) * 20.0
