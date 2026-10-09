# OpaqueSense

## 面向黑盒加密流量分析的基础模型

OpaqueSense 是一个面向黑盒加密流量分析的基础模型项目。它不访问网络流量载荷内容，而是从流量元数据、包序列模式和协议特征中学习通用表示，为下游分类任务提供统一的流量表示和推理接口。

当前项目主要面向中文安全算法、网络安全和 AI 安全工程场景。仓库提供模型核心模块、数据接口、训练模型、评估工具、推理接口和可运行的合成数据 Demo。

English version: [README_EN.md](README_EN.md)

## 项目背景

TLS 1.3、QUIC 和 ECH 等现代协议逐渐降低了传统深度包检测对流量载荷的可见性。依赖明文载荷、固定特征或人工规则的检测流程，在加密比例不断提高的网络环境中面临较大限制。

OpaqueSense 采用以下处理路径：

```text
黑盒加密流量
      ↓
包级元数据与协议特征
      ↓
字段嵌入与协议感知嵌入
      ↓
Transformer 编码器
      ↓
通用流量表示
      ↓
下游分类任务与流量推理
```

## 项目亮点

- 无需访问载荷内容的加密流量理解
- 基于 Transformer 的流量表征学习
- 通用分类头可用于恶意流量、VPN 和应用指纹等下游任务
- 提供序列表示和分类指标，便于比较不同任务的结果
- 使用合成数据展示输入格式，公开版本不包含真实流量

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
# Windows PowerShell：.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python demo/inference_demo.py --input examples/example_flow.json
```

示例输出：

```text
协议：TLS

演示输出（非训练模型预测）：
恶意流量演示分数：0.17
VPN 演示分数：0.36
应用类别示例：web_tls
```

该 Demo 用于展示输入格式、特征校验和推理流程，输出分数由可复现的演示规则生成，不代表训练模型结果。

## 输入数据格式

项目使用不包含载荷内容的流量记录。最小输入字段如下：

```json
{
  "protocol": "TLS",
  "packet_lengths": [512, 64, 128],
  "directions": [1, 0, 1],
  "iat": [0.02, 0.15, 0.03]
}
```

- `protocol`：协议类型，例如 `TLS`。预处理接口会同时生成模型使用的 `protocol_id`；
- `packet_lengths`：包长度序列；
- `directions`：包方向序列；
- `iat`：相邻数据包之间的时间间隔序列。

示例数据仅用于展示输入格式，公开版本不包含真实 PCAP、企业流量或其他敏感流量。

## 目录结构

```text
OpaqueSense/
├── README.md                 # 中文项目说明
├── README_EN.md              # 英文对照说明
├── configs/                  # 预训练、微调和推理配置
├── docs/                     # 架构、数据、训练和评估说明
├── src/
│   ├── models/               # 流量嵌入与 Transformer 模块
│   ├── dataset/              # 数据校验、特征整理和批处理接口
│   ├── training/             # 表示模型与分类头
│   ├── evaluation/           # 指标和评估工具
│   └── deployment/           # 推理接口
├── demo/                     # 可运行的推理示例
├── examples/                 # 合成流量样例
└── checkpoints/              # 模型权重目录
```

## 模型组件

`src/models/traffic_embedding.py` 提供数值流量特征和协议编号的组合嵌入；`src/models/transformer_encoder.py` 提供基于多头注意力的序列编码器；`src/evaluation/metrics.py` 提供准确率和加权 F1 指标接口。`src/dataset/preprocessing.py` 负责把协议名称转换为稳定编号。

训练目录包含表示模型和分类头，推理目录提供统一的模型调用接口。

## 内容范围

当前版本包含模型组件、配置模板和合成流量样例，不包含真实流量样本或预训练权重。

## 许可证

本项目采用 MIT License，详见 [LICENSE](LICENSE)。
