# 数据接口

## 单条流记录

每条记录以 burst 为单位，字段示例见 [`examples/example_flow.json`](../examples/example_flow.json)。`burst_tokens` 是二维整数列表，原始 token 值在 `[0,65535]`；批处理会加 1，为 padding 的 token ID 0 留出位置。其外层长度为 burst 数，内层长度为该 burst 的 token 数。`directions` 原始值为布尔值，规范化为正向 `1`、反向 `-1`；`bytes`、`iats`、`counts` 均为 burst 级一维数组，长度必须与 burst 数一致。`iats` 按 `×1e-3` 转换为整数。`protocol` 是单流的传输层协议号：ICMP=1、TCP=6、UDP=17。`labels` 可选，仅用于带标签任务。

## 批次张量

`normalize_flow()` 校验记录；`collate_flows()` 给每条 burst 前置 BOS，并按批次最大 burst 数及 burst 长度补齐后将二维 burst 结构展平为 token 轴。

| 张量 | 形状 | 说明 |
| --- | --- | --- |
| `input_ids` | `[B,L]` | token ID，含每个 burst 的 BOS |
| `attention_mask` | `[B,L]` | 真实 token 为 1，padding 为 0 |
| `direction` | `[B,L]` | burst 方向重复到该 burst 的每个位置 |
| `bytes` | `[B,L]` | burst 字节总数重复到各 token 位置 |
| `iats` | `[B,L]` | burst 间隔重复到各 token 位置 |
| `pkt_count` | `[B,L]` | burst 包数重复到各 token 位置 |
| `protocol` | `[B]` | 每条流一个协议编号 |
| `dataset_burst_sizes` | `[B,max_bursts]` | 每个 burst 的 token 数，不含前置 BOS |

`flow_duration` 保留为流级数值字段供任务使用，目前没有送入嵌入层。`labels` 也不属于无标签表示模型的输入。
