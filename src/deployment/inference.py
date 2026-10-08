"""Portable inference interface for normalized OpaqueSense features."""
from __future__ import annotations

def run(model, features):
    """Run a compatible model on a feature batch."""
    return model(features)
