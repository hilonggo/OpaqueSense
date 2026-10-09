"""校验并规范化按 burst 组织的流量记录。"""
from __future__ import annotations

from collections.abc import Mapping

import numpy as np

REQUIRED = ("flow_duration", "burst_tokens", "directions", "bytes", "iats", "counts", "protocol")
PROTOCOL_IDS = {"ICMP": 1, "TCP": 6, "UDP": 17}
BOS_TOKEN_ID = 65537
PAD_TOKEN_ID = 0


def protocol_to_id(protocol: str | int) -> int:
    """保留传输层协议号，字符串形式支持 ICMP、TCP 和 UDP。"""
    if isinstance(protocol, (int, np.integer)):
        protocol_number = int(protocol)
    else:
        name = str(protocol).strip().upper()
        if name not in PROTOCOL_IDS:
            raise ValueError(f"不支持的协议：{protocol!r}；可用值为 ICMP、TCP、UDP")
        protocol_number = PROTOCOL_IDS[name]
    if protocol_number not in PROTOCOL_IDS.values():
        raise ValueError("protocol 必须是 ICMP(1)、TCP(6) 或 UDP(17)")
    return protocol_number


def normalize_flow(flow: Mapping) -> dict:
    missing = [key for key in REQUIRED if key not in flow]
    if missing:
        raise ValueError(f"缺少流量字段：{', '.join(missing)}")
    bursts = flow["burst_tokens"]
    if not isinstance(bursts, (list, tuple)) or not bursts:
        raise ValueError("burst_tokens 必须是非空的二维 burst/token 序列")
    try:
        tokens = [np.asarray(burst, dtype=np.int64) for burst in bursts]
        directions = np.asarray(flow["directions"], dtype=np.float32)
        byte_counts = np.asarray(flow["bytes"], dtype=np.float32)
        iats = np.asarray(flow["iats"], dtype=np.float32)
        counts = np.asarray(flow["counts"], dtype=np.float32)
        duration = float(flow["flow_duration"])
    except (TypeError, ValueError) as exc:
        raise ValueError("burst token 和 burst 元数据必须是数值") from exc
    burst_count = len(tokens)
    if any(token.ndim != 1 or len(token) == 0 for token in tokens):
        raise ValueError("每个 burst_tokens 元素都必须是非空的一维 token 序列")
    if any(np.any((token < 0) | (token > 65535)) for token in tokens):
        raise ValueError("burst token 必须位于 uint16 范围 [0, 65535]")
    for name, values in (("directions", directions), ("bytes", byte_counts), ("iats", iats), ("counts", counts)):
        if values.ndim != 1 or len(values) != burst_count:
            raise ValueError(f"{name} 必须是与 burst 数量一致的一维序列")
        if not np.isfinite(values).all():
            raise ValueError(f"{name} 不能包含 NaN 或无穷值")
    if not np.isfinite(duration) or duration < 0:
        raise ValueError("flow_duration 必须是非负有限数")
    if not np.isin(directions, (0, 1, -1)).all():
        raise ValueError("directions 只能使用布尔值或 0、1、-1")
    if (byte_counts < 0).any() or (iats < 0).any() or (counts < 0).any():
        raise ValueError("bytes、iats 和 counts 不能为负数")
    return {
        "flow_duration": duration,
        "burst_tokens": tokens,
        "directions": np.where(directions == 0, -1, directions),
        "bytes": byte_counts,
        "iats": np.asarray(iats * 1e-3, dtype=np.int64),
        "counts": counts,
        "protocol": protocol_to_id(flow["protocol"]),
        **({"labels": flow["labels"]} if "labels" in flow else {}),
    }
