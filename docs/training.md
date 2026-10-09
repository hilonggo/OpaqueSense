# 训练

`src/training/pretrain.py` 提供流量表示模型，将包级特征嵌入后交给 Transformer 编码器；`src/training/finetune.py` 在序列表示上附加通用分类头。配置模板中的模型维度、层数和类别数与对应的构建函数保持一致。
