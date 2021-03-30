import numpy as np
import torch
import torch.nn as nn
from .base_model import BaseModel


class TDGammon(BaseModel):
    def __init__(self, hidden_units, alpha, lambda_param,
                 init_weights, seed=5324533, input_units=198, output_units=1):
        super(TDGammon, self).__init__(alpha, lambda_param, seed=seed)

        self.hidden = nn.Sequential(nn.Linear(input_units, hidden_units), nn.Sigmoid())
        # self.hidden2 = nn.Sequential(nn.Linear(hidden_units, hidden_units), nn.Sigmoid())
        # self.hidden3 = nn.Sequential(nn.Linear(hidden_units, hidden_units), nn.Sigmoid())

        self.output = nn.Sequential(nn.Linear(hidden_units, output_units), nn.Sigmoid())

        if init_weights:
            self.initialize_weights()

    def adjust_weights(self, p, p_next):
        # Set all gradients to zero
        self.zero_grad()
        # Compute the gradient of p with respect to the params
        p.backward()
        # Setting no grad allows for faster computation
        with torch.no_grad():
            # Get all weights of our network
            parameters = list(self.parameters())
            # Apply algorithm to all layers
            for i, weights in enumerate(parameters):
                # et+1 = lambda * et + gradient
                self.eligibility_traces[i] = self.lambda_param * self.eligibility_traces[i]\
                                             + weights.grad
                # w = w + alpha * (pt+1 -pt) * et
                new_weights = weights + self.alpha * (p_next - p) * self.eligibility_traces[i]
                # Set the updated weights
                weights.copy_(new_weights)

    def forward(self, x):
        x = torch.from_numpy(np.array(x))
        x = self.hidden(x)
        # x = self.hidden2(x)
        # x = self.hidden3(x)
        x = self.output(x)
        return x

    def initialize_weights(self):
        for param in self.parameters():
            nn.init.zeros_(param)
