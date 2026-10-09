# OpaqueSense

## A Foundation Model for Black-box Encrypted Traffic Intelligence

中文说明：[README.md](README.md)

OpaqueSense learns general-purpose representations from encrypted network traffic without inspecting payload content. The public project provides a modular Transformer pipeline for traffic embedding, representation learning, downstream classification, and inference.

Modern TLS 1.3, QUIC, and ECH reduce the visibility available to payload-oriented DPI. OpaqueSense uses flow metadata, packet-sequence patterns, and protocol-aware embeddings to produce a reusable traffic representation for malware detection, VPN identification, and application fingerprinting.

## Highlights

- Payload-independent encrypted-traffic understanding
- Transformer traffic representation learning
- A reusable classification head for downstream security tasks
- Evaluation helpers for comparing downstream predictions
- Synthetic examples with no private traffic included

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python demo/inference_demo.py --input examples/example_flow.json
```

The demo consumes a JSON flow description and runs without PCAP files or external services. Its scores are deterministic demonstration values rather than results from a trained checkpoint.

## Repository guide

- `src/models/` — packet metadata embeddings and Transformer components
- `src/dataset/` — public-data preprocessing and batching interfaces
- `src/training/` — representation model and classification head
- `src/evaluation/` — metrics and benchmark helpers
- `src/deployment/` — inference utilities
- `docs/` — architecture, data, training, and evaluation notes
- `examples/` — synthetic, payload-free flow examples

## Project scope

The current version contains model components, configuration templates, and synthetic flow examples. It does not bundle real traffic samples or pretrained weights. See `docs/dataset.md` for the feature schema.

## License

Released under the MIT License. See [LICENSE](LICENSE).
