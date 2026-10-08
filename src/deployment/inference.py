"""面向规范化 OpaqueSense 流量特征的通用推理接口。"""
from __future__ import annotations

def run(model, features):
    """使用兼容模型处理一批流量特征。"""
    return model(features)
