"""流量表示模型的构建接口。"""
from __future__ import annotations

from collections.abc import Mapping

import torch
from torch import nn

from src.models import TrafficEmbedding, TrafficTransformerEncoder


class TrafficRepresentationModel(nn.Module):
    """将包级特征编码为可供下游任务使用的序列表示。"""

    def __init__(
        self,
        vocab_size: int = 65538,
        hidden_dim: int = 128,
        protocol_vocab: int = 18,
        layers: int = 4,
        heads: int = 4,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.embedding = TrafficEmbedding(vocab_size, hidden_dim, protocol_vocab)
        self.encoder = TrafficTransformerEncoder(hidden_dim, layers, heads, dropout)

    def forward(
        self,
        input_ids: torch.Tensor,
        direction: torch.Tensor,
        iats: torch.Tensor,
        bytes_: torch.Tensor,
        pkt_count: torch.Tensor,
        protocol: torch.Tensor,
        padding_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        embedded = self.embedding(input_ids, direction, iats, bytes_, pkt_count, protocol)
        return self.encoder(embedded, padding_mask)


def build_representation_model(config: Mapping | None = None) -> TrafficRepresentationModel:
    """根据 YAML 配置字典构建表示模型。"""
    values = dict(config or {})
    keys = ("vocab_size", "hidden_dim", "protocol_vocab", "layers", "heads", "dropout")
    return TrafficRepresentationModel(**{key: values[key] for key in keys if key in values})


def masked_mean_pool(hidden_states: torch.Tensor, padding_mask: torch.Tensor | None = None) -> torch.Tensor:
    """对未填充位置求平均，得到每条流量的固定长度表示。"""
    if padding_mask is None:
        return hidden_states.mean(dim=1)
    valid = (~padding_mask).unsqueeze(-1)
    totals = (hidden_states * valid).sum(dim=1)
    counts = valid.sum(dim=1).clamp_min(1)
    return totals / counts
