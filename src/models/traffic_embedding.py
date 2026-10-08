"""Protocol-aware embedding for payload-free packet metadata."""
from __future__ import annotations
import torch
from torch import nn

class TrafficEmbedding(nn.Module):
    def __init__(self, feature_dim: int = 3, hidden_dim: int = 128, protocol_vocab: int = 32):
        super().__init__()
        self.numeric = nn.Sequential(nn.LayerNorm(feature_dim), nn.Linear(feature_dim, hidden_dim))
        self.protocol = nn.Embedding(protocol_vocab, hidden_dim)

    def forward(self, features: torch.Tensor, protocol_id: torch.Tensor) -> torch.Tensor:
        return self.numeric(features) + self.protocol(protocol_id).unsqueeze(1)
