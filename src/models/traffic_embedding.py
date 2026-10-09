"""面向不含载荷内容的包级元数据的协议感知嵌入。"""
from __future__ import annotations
import torch
from torch import nn

class TrafficEmbedding(nn.Module):
    def __init__(self, feature_dim: int = 3, hidden_dim: int = 128, protocol_vocab: int = 32):
        super().__init__()
        self.numeric = nn.Sequential(nn.LayerNorm(feature_dim), nn.Linear(feature_dim, hidden_dim))
        self.protocol = nn.Embedding(protocol_vocab, hidden_dim)

    def forward(self, features: torch.Tensor, protocol_id: torch.Tensor) -> torch.Tensor:
        if features.ndim != 3:
            raise ValueError("features 必须是 [batch, sequence, feature] 三维张量")
        if protocol_id.ndim != 1 or protocol_id.shape[0] != features.shape[0]:
            raise ValueError("protocol_id 必须是与 batch 对齐的一维张量")
        protocol_id = protocol_id.to(dtype=torch.long)
        return self.numeric(features) + self.protocol(protocol_id).unsqueeze(1)
