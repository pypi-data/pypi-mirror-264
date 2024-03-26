import torch
import torch.nn as nn
import torch.nn.functional as F
from torchdiffeq import odeint_adjoint, odeint
from .cnn import SimpleCNN

from typing import List, Optional

class CNNSolver(nn.Module):
    def __init__(self,
                 input_dim: int,
                 cnn_hidden_size: int = 64,
                 cnn_hidden_layers: int = 1,
                 solver: dict = {"method": "dopri5"},
                 use_adjoint: bool = True,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.input_dim = input_dim
        
        self.cnn = SimpleCNN(
            input_size=input_dim,
            hidden_layers=cnn_hidden_layers,
            hidden_channels=cnn_hidden_size
        )
        
        self.solver = solver
        self.use_adjoint = use_adjoint

    def _ode(self, t, x):
        return self.cnn(x)
    
    def forward(self, x, t_eval=[0.0, 1.0]):
        t_eval = torch.tensor(t_eval, dtype=x.dtype, device=x.device)
        if self.use_adjoint:
            return odeint_adjoint(self._ode, x, t_eval, **self.solver, adjoint_params=self.cnn.parameters())[1:]
        else:
            return odeint(self._ode, x, t_eval, **self.solver)[1:]