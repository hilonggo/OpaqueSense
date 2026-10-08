import torch
import torch.nn as nn

# 保留统一导入位置，便于注意力实现切换
from transformers.models.roformer.modeling_roformer import RoFormerAttention  # noqa: F401
from transformers.models.roberta.modeling_roberta import RobertaAttention  # noqa: F401

try:
    from flash_attn.modules.mha import MHA as FlashMHA
    from flash_attn.bert_padding import unpad_input, pad_input

    _FLASH_AVAILABLE = True
except Exception:
    FlashMHA = None
    _FLASH_AVAILABLE = False


class FlashSelfAttention(nn.Module):
    """
    使用去除填充的 FlashAttention 实现，用于提升计算效率。
    """
    def __init__(self, config, use_rotary=False):
        super().__init__()
        if not _FLASH_AVAILABLE or not torch.cuda.is_available():
            raise RuntimeError("FlashAttention 不可用，或当前环境缺少 CUDA")
        self.attn = FlashMHA(
            embed_dim=config.hidden_size,
            num_heads=config.num_attention_heads,
            dropout=config.attention_probs_dropout_prob,
            causal=config.is_decoder,
            rotary_emb_dim=0,
            use_flash_attn=True,
        )

    def forward(self, hidden_states, attention_mask=None, **kwargs):
        if attention_mask is not None:
            # 将扩展注意力掩码转换为布尔型填充掩码
            key_padding_mask = attention_mask.squeeze(1).squeeze(1) >= 0
            # 转换为去除填充后的表示
            hidden_unpad, indices, cu_seqlens, max_seqlen, seqused = unpad_input(hidden_states, key_padding_mask)
            out_unpad = self.attn(hidden_unpad, cu_seqlens=cu_seqlens, max_seqlen=max_seqlen)
            # 恢复为带填充的布局
            output = pad_input(out_unpad, indices, batch=hidden_states.size(0), seqlen=key_padding_mask.shape[1])
        else:
            output = self.attn(hidden_states)
        # FlashAttention 内核不返回注意力权重图
        return (output, None)
