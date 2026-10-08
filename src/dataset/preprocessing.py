"""Validation and normalization for payload-free flow features."""
from __future__ import annotations

from typing import Mapping
import numpy as np

REQUIRED = ("protocol", "packet_lengths", "directions", "iat")

def normalize_flow(flow: Mapping) -> dict:
    missing = [key for key in REQUIRED if key not in flow]
    if missing:
        raise ValueError(f"missing flow fields: {', '.join(missing)}")
    lengths = np.asarray(flow["packet_lengths"], dtype=np.float32)
    directions = np.asarray(flow["directions"], dtype=np.float32)
    iat = np.asarray(flow["iat"], dtype=np.float32)
    if not (len(lengths) == len(directions) == len(iat) > 0):
        raise ValueError("packet_lengths, directions, and iat must have equal non-zero length")
    return {"protocol": str(flow["protocol"]), "packet_lengths": lengths, "directions": directions, "iat": iat}
