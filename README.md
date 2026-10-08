# OpaqueSense

## A Foundation Model for Black-box Encrypted Traffic Intelligence

OpaqueSense learns general-purpose representations from encrypted network traffic without inspecting payload content. The public project provides a modular Transformer pipeline for traffic embedding, self-supervised pretraining, downstream security detection, open-set discovery, and edge deployment.

Modern TLS 1.3, QUIC, and ECH reduce the visibility available to payload-oriented DPI. OpaqueSense uses flow metadata, packet-sequence patterns, and protocol-aware embeddings to produce a reusable traffic representation for malware detection, VPN identification, application fingerprinting, and unknown-threat discovery.

## Highlights

- Payload-independent encrypted-traffic understanding
- Transformer traffic representation learning
- Multi-task security detection interfaces
- Open-set threat discovery hooks
- ONNX and INT8 deployment utilities
- Synthetic examples with no private traffic included

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python demo/inference_demo.py --input examples/example_flow.json
```

The demo consumes a JSON flow description and runs without PCAP files or external services. It is intended to show the public data contract and inference flow; replace the lightweight demo model with a trained checkpoint for production use.

## Repository guide

- `src/models/` — packet metadata embeddings and Transformer components
- `src/dataset/` — public-data preprocessing and batching interfaces
- `src/training/` — pretraining and downstream fine-tuning entry points
- `src/evaluation/` — metrics and benchmark helpers
- `src/deployment/` — export, quantization, and inference utilities
- `docs/` — architecture, data, training, experiments, and deployment notes
- `examples/` — synthetic, payload-free flow examples

## Data and privacy

This repository contains no real PCAP files, enterprise traffic, private checkpoints, credentials, or internal configuration. Use synthetic data or traffic that you are authorized to process. See `docs/dataset.md` for the expected feature schema.

## License

Released under the MIT License. See [LICENSE](LICENSE).
