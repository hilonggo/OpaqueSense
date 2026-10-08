# 推理 Demo

在项目根目录执行：

```bash
python demo/inference_demo.py --input examples/example_flow.json
```

Demo 会读取不包含载荷内容的合成流量记录，完成字段校验并输出协议、恶意流量概率、VPN 概率和应用类别。
