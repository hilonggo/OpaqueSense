"""将 burst 级记录整理为与模型 forward 对齐的批次张量。"""
from __future__ import annotations

from collections.abc import Sequence
import numpy as np
import torch

from .preprocessing import BOS_TOKEN_ID, PAD_TOKEN_ID


def _pad_field(values: Sequence[Sequence[float]], max_bursts: int, max_burst_length: int, pad: float = 0) -> np.ndarray:
    rows = [list(row[:max_burst_length]) + [pad] * (max_burst_length - len(row)) for row in values[:max_bursts]]
    rows += [[pad] * max_burst_length] * (max_bursts - len(rows))
    return np.asarray(rows, dtype=np.float32).reshape(-1)


def collate_flows(flows: Sequence[dict]) -> dict[str, torch.Tensor]:
    """按 batch 最大 burst 数和最大 burst 长度补齐并展平为 ``[B, L]``。"""
    if not flows:
        raise ValueError("flows 不能为空")
    max_bursts = max(len(flow["burst_tokens"]) for flow in flows)
    max_burst_length = max(len(burst) for flow in flows for burst in flow["burst_tokens"]) + 1
    input_ids, attention, directions, bytes_, iats, counts, sizes = [], [], [], [], [], [], []
    protocols, durations = [], []
    for flow in flows:
        # Reserve token ID 0 for padding; raw uint16 values become IDs 1..65536.
        bursts = [[BOS_TOKEN_ID] + [int(token) + 1 for token in burst] for burst in flow["burst_tokens"]]
        input_ids.append(_pad_field(bursts, max_bursts, max_burst_length, PAD_TOKEN_ID))
        attention.append(_pad_field([[1] * len(burst) for burst in bursts], max_bursts, max_burst_length, 0))
        sizes.append([len(burst) for burst in flow["burst_tokens"]] + [0] * (max_bursts - len(flow["burst_tokens"])))
        for target, key in ((directions, "directions"), (bytes_, "bytes"), (iats, "iats"), (counts, "counts")):
            expanded = [[value] * len(burst) for value, burst in zip(flow[key], flow["burst_tokens"])]
            target.append(_pad_field([[value] + row for value, row in zip(flow[key], expanded)], max_bursts, max_burst_length, 0))
        protocols.append(flow["protocol"])
        durations.append(flow["flow_duration"])
    return {
        "input_ids": torch.tensor(np.asarray(input_ids), dtype=torch.long),
        "attention_mask": torch.tensor(np.asarray(attention), dtype=torch.long),
        "direction": torch.tensor(np.asarray(directions), dtype=torch.float32),
        "bytes": torch.tensor(np.asarray(bytes_), dtype=torch.float32),
        "iats": torch.tensor(np.asarray(iats), dtype=torch.float32),
        "pkt_count": torch.tensor(np.asarray(counts), dtype=torch.float32),
        "protocol": torch.tensor(protocols, dtype=torch.long),
        "flow_duration": torch.tensor(durations, dtype=torch.float32),
        "dataset_burst_sizes": torch.tensor(np.asarray(sizes), dtype=torch.long),
    }
