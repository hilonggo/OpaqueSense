# 模型架构

OpaqueSense 面向黑盒流量分析，将一条流表示为按时间排列的 burst/token 记录。批处理时保留各 burst 的边界信息，同时将 burst 依次展平到 token 序列维度。每个 token 位置融合 token ID、方向/字节数/间隔/包数四项 burst 元数据和单流协议嵌入，Transformer 再对序列上下文进行编码。

```text
单条记录
  burst_tokens: [[token...], [token...], ...]
  burst 元数据: directions / bytes / iats / counts
  protocol: 单个协议号
             ↓ normalize_flow + collate_flows
  input_ids [B,L]       attention_mask [B,L]
  direction [B,L]       bytes [B,L]
  iats [B,L]            pkt_count [B,L]
  protocol [B]
             ↓
  token embedding + 元数据 MLP + 协议 embedding
             ↓
  特征压缩与 Transformer 编码
             ↓
  序列表示 → 池化 → 下游分类头
```

对应实现：

- `src/dataset/preprocessing.py`：检查 burst/token 记录并映射协议号；
- `src/dataset/dataloader.py`：添加 BOS、按 batch 补齐并展平 burst；
- `src/models/traffic_embedding.py`：融合 token、burst 元数据和协议嵌入；
- `src/models/transformer_encoder.py`：对 `[B,L,H]` 序列编码；
- `src/training/pretrain.py`、`src/training/finetune.py`：表示模型与分类器。

架构示意图见 [architecture.png](architecture.png)。
