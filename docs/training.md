# 训练

`src/training/pretrain.py` 的表示模型接收 collator 生成的 token ID、方向、字节数、间隔、包数和协议张量；序列字段形状为 `[B,L]`，协议形状为 `[B]`，可选 padding mask 为 `[B,L]`。`src/training/finetune.py` 使用同一输入接口并在序列池化后输出分类 logits。模型维度等参数见 `configs/`。
