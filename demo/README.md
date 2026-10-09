# 推理 Demo

在项目根目录执行：

```bash
python demo/inference_demo.py --input examples/example_flow.json
```

示例会读取 burst/token 流量记录，完成字段校验，并输出补齐后 `input_ids` 和 `attention_mask` 的形状。该示例不加载权重或输出分类预测。
