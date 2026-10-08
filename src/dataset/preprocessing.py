"""校验并规范化不含载荷内容的流量特征。"""
from __future__ import annotations

from typing import Mapping
import numpy as np

REQUIRED = ("protocol", "packet_lengths", "directions", "iat")

def normalize_flow(flow: Mapping) -> dict:
    missing = [key for key in REQUIRED if key not in flow]
    if missing:
        raise ValueError(f"缺少流量字段：{', '.join(missing)}")
    lengths = np.asarray(flow["packet_lengths"], dtype=np.float32)
    directions = np.asarray(flow["directions"], dtype=np.float32)
    iat = np.asarray(flow["iat"], dtype=np.float32)
    if not (len(lengths) == len(directions) == len(iat) > 0):
        raise ValueError("packet_lengths、directions 和 iat 必须具有相同且非零的长度")
    return {"protocol": str(flow["protocol"]), "packet_lengths": lengths, "directions": directions, "iat": iat}
