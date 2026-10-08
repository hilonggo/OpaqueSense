"""Small batching helpers for normalized flow dictionaries."""
from __future__ import annotations
import numpy as np

def flow_features(flow: dict) -> np.ndarray:
    return np.stack([flow["packet_lengths"], flow["directions"], flow["iat"]], axis=-1)
