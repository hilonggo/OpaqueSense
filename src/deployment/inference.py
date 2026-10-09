"""面向规范化 burst/token 记录的通用推理接口。"""
from __future__ import annotations

def run(model, batch):
    """将 ``collate_flows`` 生成的批次传入兼容模型。"""
    return model(
        batch["input_ids"], batch["direction"], batch["iats"], batch["bytes"],
        batch["pkt_count"], batch["protocol"],
        padding_mask=batch["attention_mask"].eq(0),
    )
