# OpaqueSense

## Foundation model for black-box encrypted traffic analysis

OpaqueSense uses flow records organized as **bursts**. Protocol is a per-flow integer input, separate from the token sequence, and is fused with token and burst metadata embeddings.

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
