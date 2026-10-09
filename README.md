# OpaqueSense

## 面向黑盒加密流量分析的基础模型

OpaqueSense 使用按 **burst** 组织的流量记录学习通用表示。模型不要求把协议名称拼进 token 序列：协议是每条流独立的整数输入，和 token、burst 级元数据一起进入嵌入层。

English version: [README_EN.md](README_EN.md)

## 数据输入

每条流对应一条 JSON 记录，字段与项目的批处理接口一致：

```json
{
  "flow_duration": 183,
  "burst_tokens": [[450, 12, 2048, 33], [9, 1024, 18]],
  "directions": [1, 0],
  "bytes": [2560, 1033],
  "iats": [0, 42],
  "counts": [4, 3],
  "protocol": 6,
  "labels": "示例"
}
```

- `flow_duration`：整条流的持续时间；
- `burst_tokens`：二维数组，形状为 `[burst 数量, token 数量]`，每个原始 token 是 `[0,65535]` 的整数；批处理会将其加 1，为 padding 的 0 留出编号；
- `directions`：每个 burst 的方向，原始记录使用布尔值；校验后转换为正向 `1`、反向 `-1`；
- `bytes`：每个 burst 的字节数；
- `iats`：每个 burst 的间隔值；预处理按原始 tokenizer 口径乘以 `1e-3` 并转为整数；
- `counts`：每个 burst 的包数量；
- `protocol`：独立的传输层协议编号，支持 ICMP=`1`、TCP=`6`、UDP=`17`；
- `labels`：可选的下游任务标签。

`directions`、`bytes`、`iats` 和 `counts` 的长度必须等于 burst 数量。`labels` 不参与输入嵌入，仅用于带标签任务。

## 模型输入形状

`collate_flows()` 按一个 batch 的最大 burst 数和最大 burst 长度补齐，并把 burst 展平为 token 轴：

| 字段 | 形状 | 含义 |
| --- | --- | --- |
| `input_ids` | `[B, L]` | 每个 burst 前加 BOS 后的 token 序列 |
| `attention_mask` | `[B, L]` | 有效 token 为 1，补齐位置为 0 |
| `direction` | `[B, L]` | burst 方向展开到 token 位置 |
| `bytes` | `[B, L]` | burst 字节数展开到 token 位置 |
| `iats` | `[B, L]` | burst 间隔展开到 token 位置 |
| `pkt_count` | `[B, L]` | burst 包数展开到 token 位置 |
| `protocol` | `[B]` | 每条流一个协议编号 |
| `dataset_burst_sizes` | `[B, max_bursts]` | 原始 burst 长度，用于恢复 burst 边界 |

模型调用形式为 `model(input_ids, direction, iats, bytes, pkt_count, protocol, padding_mask=...)`。协议字段因此是模型输入的一部分，但维度是 `[B]`，不是 `[B,L]` 的 token 序列列。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell：.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python demo/inference_demo.py --input examples/example_flow.json
```

示例会校验记录并打印 `input_ids`、`attention_mask` 的批次形状，不加载权重，也不伪造分类结果。

## 处理流程

```text
burst/token 流量记录
        ↓
字段校验与 burst 补齐
        ↓
[B,L] token + [B,L] burst 元数据 + [B] 协议
        ↓
token、元数据、协议嵌入融合
        ↓
Transformer 编码器
        ↓
流量表示与下游分类
```

## 目录结构

```text
OpaqueSense/
├── README.md
├── README_EN.md
├── configs/                  # 模型与任务配置
├── docs/                     # 数据、架构、训练和评估说明
├── src/
│   ├── models/               # token、元数据和 Transformer 模块
│   ├── dataset/              # burst 校验与 [B,L] 批处理
│   ├── training/             # 表示模型与分类头
│   ├── evaluation/           # 评估指标
│   └── deployment/           # 批次推理接口
├── demo/                     # 输入检查示例
├── examples/                 # burst/token 示例记录
└── checkpoints/              # 权重目录
```

## 许可证

本项目采用 MIT License，详见 [LICENSE](LICENSE)。
