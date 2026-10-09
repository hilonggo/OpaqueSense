"""面向批量流量序列的多头自注意力模块。"""
from __future__ import annotations

import torch
from torch import nn


class TrafficSelfAttention(nn.Module):
    """对包序列执行自注意力，并保留残差连接与层归一化。"""

    def __init__(self, hidden_dim: int = 128, heads: int = 4, dropout: float = 0.1):
        super().__init__()
        self.attention = nn.MultiheadAttention(
            embed_dim=hidden_dim,
            num_heads=heads,
            dropout=dropout,
            batch_first=True,
        )
        self.dropout = nn.Dropout(dropout)
        self.norm = nn.LayerNorm(hidden_dim)

    def forward(
        self,
        hidden_states: torch.Tensor,
        padding_mask: torch.Tensor | None = None,
        need_weights: bool = False,
    ):
        attended, weights = self.attention(
            hidden_states,
            hidden_states,
            hidden_states,
            key_padding_mask=padding_mask,
            need_weights=need_weights,
        )
        output = self.norm(hidden_states + self.dropout(attended))
        if need_weights:
            return output, weights
        return output


MultiHeadSelfAttention = TrafficSelfAttention
