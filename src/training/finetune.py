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
        feature_dim: int = 3,
        hidden_dim: int = 128,
        protocol_vocab: int = 32,
        layers: int = 4,
        heads: int = 4,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.representation = TrafficRepresentationModel(
            feature_dim, hidden_dim, protocol_vocab, layers, heads, dropout
        )
        self.classifier = nn.Linear(hidden_dim, num_classes)

    def forward(
        self,
        features: torch.Tensor,
        protocol_id: torch.Tensor,
        padding_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        sequence = self.representation(features, protocol_id, padding_mask)
        pooled = masked_mean_pool(sequence, padding_mask)
        return self.classifier(pooled)


def build_classifier(config: Mapping | None = None) -> TrafficClassifier:
    """根据微调配置字典构建分类器。"""
    values = dict(config or {})
    keys = ("num_classes", "feature_dim", "hidden_dim", "protocol_vocab", "layers", "heads", "dropout")
    return TrafficClassifier(**{key: values[key] for key in keys if key in values})
