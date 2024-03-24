from torch import nn

from kappamodules.init import init_xavier_uniform_merged_linear, init_truncnormal_zero_bias
from kappamodules.utils.shapes import to_ndim


class Film(nn.Module):
    def __init__(self, dim_cond, dim_out, init_weights="xavier_uniform"):
        super().__init__()
        self.dim_cond = dim_cond
        self.dim_out = dim_out
        self.modulation = nn.Linear(dim_cond, dim_out * 2)
        self.init_weights = init_weights
        self.reset_parameters()

    def reset_parameters(self):
        if self.init_weights == "torch":
            pass
        elif self.init_weights == "xavier_uniform":
            init_xavier_uniform_merged_linear(self.modulation, num_layers=2)
        elif self.init_weights in ["truncnormal", "truncnormal002"]:
            self.apply(init_truncnormal_zero_bias)
        else:
            raise NotImplementedError

    def forward(self, x, cond):
        scale, shift = to_ndim(self.modulation(cond), ndim=x.ndim).chunk(2, dim=1)
        return x * (scale + 1) + shift
