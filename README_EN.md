# OpaqueSense

## Traffic representation model for black-box encrypted traffic analysis

OpaqueSense targets traffic-analysis settings where applications cannot rely directly on cleartext payloads. It provides a Transformer-based representation pipeline built around **burst/token sequences, protocol context, and burst-level traffic metadata**. A flow is represented by time-ordered burst tokens together with direction, byte count, inter-burst timing, and packet-count signals; the transport protocol is supplied as a separate per-flow condition. The resulting flow representation can be connected to downstream tasks such as malicious-traffic detection, VPN analysis, and application fingerprinting.

The project treats the data path and model interface as one design: validation and collation preserve burst boundaries while producing padded `[B,L]` tensors; the embedding layer combines token, metadata, and protocol representations; the Transformer models sequence context; and a task head adapts the representation to a specific security classification problem.

### Highlights

- Encrypted-traffic modeling without relying on decrypted application-layer semantics
- Protocol-aware multi-branch embeddings with a per-flow protocol condition
- Burst boundaries retained through BOS markers and `dataset_burst_sizes`
- Explicit preprocessing, batching, masking, representation, classification, and inference interfaces
- A reusable flow representation for security-algorithm and network-security tasks

中文说明：[README.md](README.md)

## Input record

```json
{
  "flow_duration": 183,
  "burst_tokens": [[450, 12, 2048, 33], [9, 1024, 18]],
  "directions": [1, 0],
  "bytes": [2560, 1033],
  "iats": [0, 42],
  "counts": [4, 3],
  "protocol": 6,
  "labels": "example"
}
```

`burst_tokens` is a two-dimensional list of raw values in `[0,65535]`; batching shifts them by one to reserve token ID 0 for padding. `directions` uses booleans in the raw record and is normalized to `1` (forward) or `-1` (reverse). The four burst metadata arrays have one value per burst. `iats` follows the source unit conversion (`×1e-3`, integer). `protocol` is ICMP=`1`, TCP=`6`, or UDP=`17`; `labels` is optional.

## Model tensors

`collate_flows()` pads each batch and flattens bursts into the token axis:

| Field | Shape |
| --- | --- |
| `input_ids`, `attention_mask` | `[B,L]` |
| `direction`, `bytes`, `iats`, `pkt_count` | `[B,L]` |
| `protocol` | `[B]` |
| `dataset_burst_sizes` | `[B,max_bursts]` |

The model call is `model(input_ids, direction, iats, bytes, pkt_count, protocol, padding_mask=...)`.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo/inference_demo.py --input examples/example_flow.json
```

The demo validates the record and prints padded tensor shapes without loading weights or producing predictions.

## Pipeline

```text
burst/token record → validation and padding → [B,L] token and metadata + [B] protocol
→ fused embeddings → Transformer encoder → flow representation → downstream head
```

## License

MIT License. See [LICENSE](LICENSE).
