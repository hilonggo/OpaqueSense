from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.dataset import collate_flows, normalize_flow

def main():
    parser = argparse.ArgumentParser(description="检查 burst/token 流量输入并展示模型批次形状")
    parser.add_argument("--input", required=True, help="JSON 流量样例路径")
    args = parser.parse_args()
    flow = normalize_flow(json.loads(Path(args.input).read_text(encoding="utf-8")))
    batch = collate_flows([flow])
    print(f"协议编号：{flow['protocol']}")
    print(f"burst 数量：{len(flow['burst_tokens'])}")
    print(f"input_ids 形状：{tuple(batch['input_ids'].shape)}")
    print(f"attention_mask 形状：{tuple(batch['attention_mask'].shape)}")
    print("该示例只验证输入整理，不加载训练权重，也不输出分类预测。")

if __name__ == "__main__":
    main()
