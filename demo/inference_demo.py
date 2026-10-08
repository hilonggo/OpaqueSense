from __future__ import annotations
import argparse, json
from pathlib import Path
from src.dataset.preprocessing import normalize_flow

def predict(flow):
    lengths = flow["packet_lengths"]
    burstiness = float(lengths.std() / (lengths.mean() + 1e-6))
    vpn = min(0.99, max(0.01, 0.25 + 0.12 * burstiness))
    malware = min(0.99, max(0.01, 0.10 + 0.08 * burstiness + 0.03 * (len(lengths) > 8)))
    return malware, vpn, "web_tls" if flow["protocol"].upper() == "TLS" else "unknown"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    flow = normalize_flow(json.loads(Path(args.input).read_text(encoding="utf-8")))
    malware, vpn, app = predict(flow)
    print(f"协议：{flow['protocol']}")
    print("\n预测结果：")
    print(f"恶意流量概率：{malware:.2f}")
    print(f"VPN概率：{vpn:.2f}")
    print(f"应用类别：{app}")

if __name__ == "__main__":
    main()
