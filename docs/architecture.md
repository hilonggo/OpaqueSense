# 模型架构

OpaqueSense 将每条流量表示为一组按时间排列的包级特征。每个时间步包含包长度、方向和包间隔时间；`normalize_flow` 将协议名称转换为稳定的 `protocol_id`，再通过独立的嵌入表加入序列表示。

处理流程如下：

```text
包级特征
   ↓
数值特征嵌入 + 协议嵌入
   ↓
Transformer 编码器
   ↓
包序列表示
   ↓
平均池化
   ↓
下游分类头
```

对应实现位于 `src/models/` 和 `src/training/`：

- `TrafficEmbedding` 将数值特征映射到隐藏空间，并加入协议嵌入；
- `TrafficTransformerEncoder` 建模包序列中的上下文关系；
- `TrafficClassifier` 对序列表示进行池化并输出类别 logits；
- `TrafficSelfAttention` 提供独立的多头自注意力模块。

架构示意图见 [architecture.png](architecture.png)。
