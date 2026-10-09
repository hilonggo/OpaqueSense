"""用于包序列表示学习的 Transformer 编码器。"""
from torch import nn

class TrafficTransformerEncoder(nn.Module):
    def __init__(self, hidden_dim=128, layers=4, heads=4, dropout=0.1):
        super().__init__()
        layer = nn.TransformerEncoderLayer(hidden_dim, heads, dim_feedforward=4 * hidden_dim, dropout=dropout, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=layers)

    def forward(self, x, padding_mask=None):
        return self.encoder(x, src_key_padding_mask=padding_mask)
