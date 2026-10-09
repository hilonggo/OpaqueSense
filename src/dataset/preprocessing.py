"""校验并规范化不含载荷内容的流量特征。"""
from __future__ import annotations

from typing import Mapping
import numpy as np

REQUIRED = ("protocol", "packet_lengths", "directions", "iat")
PROTOCOL_IDS = {"TLS": 0, "QUIC": 1, "TCP": 2, "UDP": 3, "DNS": 4, "HTTP": 5}


def protocol_to_id(protocol: str, vocabulary_size: int = 32) -> int:
    """将协议名称映射为模型使用的稳定整数编号。"""
    if vocabulary_size < 2:
        raise ValueError("vocabulary_size 必须至少为 2")
    normalized = str(protocol).strip().upper()
    if not normalized:
        raise ValueError("protocol 不能为空")
    return PROTOCOL_IDS.get(normalized, vocabulary_size - 1)

def normalize_flow(flow: Mapping) -> dict:
    missing = [key for key in REQUIRED if key not in flow]
    if missing:
        raise ValueError(f"缺少流量字段：{', '.join(missing)}")
    protocol = str(flow["protocol"]).strip()
    if not protocol:
        raise ValueError("protocol 不能为空")
    try:
        lengths = np.asarray(flow["packet_lengths"], dtype=np.float32)
        directions = np.asarray(flow["directions"], dtype=np.float32)
        iat = np.asarray(flow["iat"], dtype=np.float32)
    except (TypeError, ValueError) as exc:
        raise ValueError("流量数值字段必须是可转换为浮点数的一维序列") from exc
    if not (lengths.ndim == directions.ndim == iat.ndim == 1):
        raise ValueError("packet_lengths、directions 和 iat 必须是一维序列")
    if not (len(lengths) == len(directions) == len(iat) > 0):
        raise ValueError("packet_lengths、directions 和 iat 必须具有相同且非零的长度")
    if not (np.isfinite(lengths).all() and np.isfinite(directions).all() and np.isfinite(iat).all()):
        raise ValueError("流量数值字段不能包含 NaN 或无穷值")
    if (lengths < 0).any() or (iat < 0).any():
        raise ValueError("packet_lengths 和 iat 不能为负数")
    if not np.isin(directions, (0, 1)).all():
        raise ValueError("directions 只能包含 0 或 1")
    return {"protocol": protocol, "protocol_id": protocol_to_id(protocol), "packet_lengths": lengths, "directions": directions, "iat": iat}
