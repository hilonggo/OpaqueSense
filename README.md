# OpaqueSense

## 面向黑盒加密流量分析的流量表征模型

OpaqueSense 面向无法直接依赖明文载荷的网络流量分析场景，提供一套以 **burst/token 序列为核心、协议与流量元数据为条件** 的 Transformer 表征模型。它把一条流中按时间排列的 burst token、方向、字节数、时间间隔和包数量整理为统一的批次张量，并将整条流的传输层协议作为独立条件输入，编码为可供恶意流量识别、VPN 流量分析、应用指纹等下游任务复用的流量表示。

项目的重点不是依赖某个固定的分类规则，而是把网络流量的序列结构、burst 边界和协议上下文纳入同一个建模接口：数据层负责严格校验和补齐，嵌入层分别处理 token、burst 元数据与协议信息，Transformer 负责建模长序列中的上下文关系，分类头则在流级表示上适配具体安全任务。

### 项目亮点

- **面向加密流量分析**：通过 token 化流量和 burst 统计特征建模，不依赖解密后的应用层明文语义。
- **协议感知的多路嵌入**：协议不是被拼接进 token 序列的字符串，而是以 `[B]` 的流级条件进入协议嵌入，并广播到对应流的序列位置。
- **保留 burst 结构**：每个 burst 使用独立的起始标记，批处理保留 burst 长度信息，同时将序列规范化为 `[B,L]`，便于 Transformer 训练和推理。
- **从数据到模型的完整接口**：包含记录校验、批次补齐、`attention_mask`、表示模型、下游分类头和推理适配器，输入输出的字段与张量形状明确可查。
- **便于安全算法工程落地**：同一套流量表示可接入不同的检测、识别和分类任务，便于在统一数据接口下替换任务头、比较模型配置和扩展评估指标。

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
