"""按原始 burst/token 接口组合 token、burst 元数据和协议嵌入。"""
from __future__ import annotations
import torch
from torch import nn

class TrafficEmbedding(nn.Module):
    def __init__(self, vocab_size: int = 65538, hidden_dim: int = 128, protocol_vocab: int = 18):
        super().__init__()
        self.tokens = nn.Embedding(vocab_size, hidden_dim)
        self.meta = nn.Sequential(nn.LayerNorm(4), nn.Linear(4, hidden_dim), nn.GELU(), nn.Linear(hidden_dim, hidden_dim))
        self.protocol = nn.Embedding(protocol_vocab, hidden_dim)
        self.compress = nn.Linear(hidden_dim * 3, hidden_dim)

    def forward(self, input_ids: torch.Tensor, direction: torch.Tensor, iats: torch.Tensor,
                bytes_: torch.Tensor, pkt_count: torch.Tensor, protocol: torch.Tensor) -> torch.Tensor:
        if input_ids.ndim != 2:
            raise ValueError("input_ids 必须是 [batch, sequence] 二维张量")
        if protocol.ndim != 1 or protocol.shape[0] != input_ids.shape[0]:
            raise ValueError("protocol 必须是与 batch 对齐的一维张量")
        meta = torch.stack([direction, bytes_ / 1000, pkt_count, iats], dim=-1).to(self.tokens.weight.dtype)
        token_embeddings = self.tokens(input_ids)
        meta_embeddings = self.meta(meta)
        protocol_embeddings = self.protocol(protocol.to(torch.long)).unsqueeze(1).expand(-1, input_ids.shape[1], -1)
        return self.compress(torch.cat([token_embeddings, meta_embeddings, protocol_embeddings], dim=-1))
