"""下游流量分类头。"""
from __future__ import annotations

from collections.abc import Mapping

import torch
from torch import nn

from .pretrain import TrafficRepresentationModel, masked_mean_pool


class TrafficClassifier(nn.Module):
    """在流量表示上附加一个通用的多类别分类头。"""

    def __init__(
        self,
        num_classes: int = 2,
        vocab_size: int = 65538,
        hidden_dim: int = 128,
        protocol_vocab: int = 18,
        layers: int = 4,
        heads: int = 4,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.representation = TrafficRepresentationModel(
            vocab_size, hidden_dim, protocol_vocab, layers, heads, dropout
        )
        self.classifier = nn.Linear(hidden_dim, num_classes)

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
        sequence = self.representation(input_ids, direction, iats, bytes_, pkt_count, protocol, padding_mask)
        pooled = masked_mean_pool(sequence, padding_mask)
        return self.classifier(pooled)


def build_classifier(config: Mapping | None = None) -> TrafficClassifier:
    """根据微调配置字典构建分类器。"""
    values = dict(config or {})
    keys = ("num_classes", "vocab_size", "hidden_dim", "protocol_vocab", "layers", "heads", "dropout")
    return TrafficClassifier(**{key: values[key] for key in keys if key in values})
