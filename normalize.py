"""
Normalization engine for the systematic review:
"Local LLM Inference on Consumer-Class GPUs"

Converts heterogeneous reported throughput numbers onto a common basis:
  - bytes/token (weight traffic)
  - Model Bandwidth Utilization (MBU)
  - bandwidth-normalized throughput (tok/s per TB/s)
  - energy per token (J/tok)
  - cost per million tokens (USD/MTok)
"""
import json, math
import pandas as pd

# ---------------------------------------------------------------
# Table 1: consumer GPU hardware substrate (vendor specifications)
# ---------------------------------------------------------------
GPUS = [
    # name, arch, VRAM GB, BW GB/s, TDP W, MSRP USD, launch
    ("RTX 3060 12GB", "Ampere",   12,  360, 170,  329, 2021),
    ("RTX 3090",      "Ampere",   24,  936, 350, 1499, 2020),
    ("RTX 4060 Ti 16GB","Ada",    16,  288, 165,  499, 2023),
    ("RTX 4070",      "Ada",      12,  504, 200,  599, 2023),
    ("RTX 4080",      "Ada",      16,  717, 320, 1199, 2022),
    ("RTX 4090",      "Ada",      24, 1008, 450, 1599, 2022),
    ("RTX 5060 Ti 16GB","Blackwell",16,448, 180,  429, 2025),
    ("RTX 5070",      "Blackwell",12,  672, 250,  549, 2025),
    ("RTX 5070 Ti",   "Blackwell",16,  896, 300,  749, 2025),
    ("RTX 5080",      "Blackwell",16,  960, 360,  999, 2025),
    ("RTX 5090",      "Blackwell",32, 1792, 575, 1999, 2025),
]
gpu = pd.DataFrame(GPUS, columns=["gpu","arch","vram_gb","bw_gbs","tdp_w","msrp_usd","year"])
gpu["bw_per_dollar"] = gpu.bw_gbs / gpu.msrp_usd
gpu["bw_per_watt"]   = gpu.bw_gbs / gpu.tdp_w
gpu["gb_per_dollar"] = gpu.vram_gb / gpu.msrp_usd

# ---------------------------------------------------------------
# Effective bits per weight for each quantization format
# (container overhead included: scales, zero-points, block metadata)
# ---------------------------------------------------------------
BPW = {
    "FP16":   16.00, "BF16": 16.00,
    "FP8":     8.00, "INT8":  8.51,   # W8A16 w/ group scales
    "Q8_0":    8.50,
    "Q6_K":    6.56,
    "Q5_K_M":  5.68,
    "Q4_K_M":  4.83,   # llama.cpp k-quant, measured file size basis
    "Q4_0":    4.55,
    "IQ4_XS":  4.25,
    "GPTQ-4":  4.25,   # g128 + zero points
    "AWQ-4":   4.25,
    "EXL2-4.65":4.65,
    "NVFP4":   4.50,   # E2M1 + FP8 micro-block scales + FP32 per-tensor
    "MXFP4":   4.25,
    "IQ3_M":   3.66,
    "IQ2_M":   2.70,
}

# Effective bits per weight is a property of a (model, container) pair, not of a
# container alone, because the share of parameters a container leaves in full
# precision -- embeddings and the output projection, above all -- varies with
# vocabulary size. Where a published artifact exists for the exact pair, we
# measure it: b = 8 * file_bytes / params. These override the generic table.
#
#   (model, container) -> (artifact bytes, source)
BPW_MEASURED = {
    ("Mistral-7B", "AWQ-4"):
        (4.15e9, "TheBloke/Mistral-7B-Instruct-v0.2-AWQ, model.safetensors"),
    ("Mistral-7B", "Q4_K_M"):
        (4.37e9, "TheBloke/Mistral-7B-Instruct-v0.2-GGUF, Q4_K_M"),
}

def bits_per_weight(model, fmt):
    """Effective bits per weight: measured from the artifact for this exact
    (model, container) pair where one is published, else the generic value."""
    key = (model, fmt)
    if key in BPW_MEASURED:
        size, _ = BPW_MEASURED[key]
        return 8.0 * size / (MODELS[model]["params"] * 1e9)
    return BPW[fmt]

# ---------------------------------------------------------------
# KV-cache traffic per token (bytes), MHA/GQA aware
# ---------------------------------------------------------------
def kv_bytes_per_token(n_layers, n_kv_heads, head_dim, bits=16):
    """Per-layer-set KV bytes added by one token: 2 tensors (K and V)."""
    return 2 * n_layers * n_kv_heads * head_dim * (bits / 8.0)

def kv_bytes_at_context(model, ctx, bits=16):
    """Total KV cache bytes held at context `ctx`, honouring sliding windows.
    Gemma 3 keeps one full-attention layer per `pat` layers; the rest cap their
    cache at `win` tokens, so the cache stops growing linearly past the window."""
    m = MODELS[model]
    per_layer_token = 2 * m["kvh"] * m["hd"] * (bits / 8.0)
    if m.get("win"):
        n_full  = max(1, round(m["L"] / m["pat"]))
        n_local = m["L"] - n_full
        tokens  = n_full * ctx + n_local * min(ctx, m["win"])
    else:
        tokens = m["L"] * ctx
    return per_layer_token * tokens

# ---------------------------------------------------------------
# Model architectural registry (dense + MoE)
# ---------------------------------------------------------------
# Architectures below were read from each model's published config.json in
# October 2026. `win` is the sliding-window span and `pat` the number of layers
# per full-attention layer (Gemma 3 interleaves 5 local layers per global one);
# win=None means every layer attends over the whole context.
MODELS = {
    "Mistral-7B":      dict(params=7.24,  active=7.24,  L=32, kvh=8,  hd=128, win=None, pat=1),
    "Llama-3-8B":      dict(params=8.03,  active=8.03,  L=32, kvh=8,  hd=128, win=None, pat=1),
    "Llama-3.1-8B":    dict(params=8.03,  active=8.03,  L=32, kvh=8,  hd=128, win=None, pat=1),
    "Qwen3-8B":        dict(params=8.19,  active=8.19,  L=36, kvh=8,  hd=128, win=None, pat=1),
    "Gemma-3-12B":     dict(params=12.2,  active=12.2,  L=48, kvh=8,  hd=256, win=1024, pat=6),
    "Gemma-3-27B":     dict(params=27.4,  active=27.4,  L=62, kvh=16, hd=128, win=1024, pat=6),
    "Qwen2.5-32B":     dict(params=32.8,  active=32.8,  L=64, kvh=8,  hd=128, win=None, pat=1),
    "OPT-30B":         dict(params=30.0,  active=30.0,  L=48, kvh=56, hd=128, win=None, pat=1),
    # --- architectures added for the non-normalizable candidate set (Table 2b).
    # Read from each model's published config.json in October 2026. gpt-oss
    # interleaves sliding and full attention on alternate layers (layer_types in
    # the config), so pat=2 and win=128 -- an unusually short window, which makes
    # these models' cache almost context-independent.
    "gpt-oss-20b":     dict(params=21.0,  active=3.6,  L=24, kvh=8,  hd=64,  win=128, pat=2),
    "gpt-oss-120b":    dict(params=117.0, active=5.1,  L=36, kvh=8,  hd=64,  win=128, pat=2),
    # Qwen3-30B-A3B: 128 experts, 8 active per token; sliding_window null.
    # 3.3B active / 30.5B total is reproduced from the config's own dimensions.
    "Qwen3-30B-A3B":   dict(params=30.5,  active=3.3,  L=48, kvh=4,  hd=128, win=None, pat=1),
    "Llama-3.3-70B":   dict(params=70.6,  active=70.6,  L=80, kvh=8,  hd=128, win=None, pat=1),
}

def weight_bytes_per_token(model, fmt, moe_resident=True):
    """Bytes of weight traffic streamed per decoded token at batch=1.
    Dense: all params. MoE: only active params if experts are resident."""
    m = MODELS[model]
    b = bits_per_weight(model, fmt) / 8.0
    p = (m["active"] if moe_resident else m["params"]) * 1e9
    return p * b

def ctx_bar(l_prompt, l_gen):
    """Mean cache occupancy over a run: the cache is already `l_prompt` deep when
    the first token is decoded and grows to `l_prompt + l_gen`, so its mean depth
    is `l_prompt + l_gen/2`.

    This is the only place the averaging over a generation happens. `bytes_per_token`
    takes the result and evaluates the cache at that depth; it must NOT halve again.
    An earlier revision did both, understating cache traffic by a factor approaching
    two on prompt-heavy workloads."""
    return l_prompt + l_gen / 2.0

def bytes_per_token(model, fmt, ctx, kv_bits=16, moe_resident=True):
    """Memory traffic per decoded token, in bytes.

    `ctx` is MEAN cache occupancy C-bar (use ctx_bar()), not the final context
    length. Attention re-reads the whole live cache at every step, so the cache
    traffic a step pays is the cache size at that step's depth; averaged over the
    run that is the cache size at mean depth. The averaging lives in C-bar, so no
    further division is applied here.

    Caveat for windowed models: kv_bytes_at_context is linear in ctx below the
    window and flat above it, so evaluating at C-bar is exact whenever the run
    stays wholly on one side of the window and approximate only when it straddles
    it. No corpus row uses a windowed model, so every tabulated value is exact."""
    w = weight_bytes_per_token(model, fmt, moe_resident)
    kv = kv_bytes_at_context(model, ctx, kv_bits)
    return w, kv, w + kv

def mbu(tok_s, model, fmt, bw_gbs, ctx, kv_bits=16, moe_resident=True):
    """Model Bandwidth Utilization: achieved memory traffic / peak bandwidth."""
    _, _, bpt = bytes_per_token(model, fmt, ctx, kv_bits, moe_resident)
    achieved = tok_s * bpt              # bytes/s
    peak = bw_gbs * 1e9
    return achieved / peak

def roofline_tok_s(model, fmt, bw_gbs, ctx, kv_bits=16, moe_resident=True):
    """Bandwidth-bound ceiling on decode throughput at batch=1."""
    _, _, bpt = bytes_per_token(model, fmt, ctx, kv_bits, moe_resident)
    return (bw_gbs * 1e9) / bpt

def vram_footprint(model, fmt, ctx, kv_bits=16, overhead_gb=1.0):
    """Static VRAM demand: weights + KV cache at full context + runtime overhead."""
    m = MODELS[model]
    # Use the measured width for this (model, container) pair where an artifact
    # has been measured, and the generic table otherwise -- the same rule
    # equation (1) follows. Using BPW[fmt] here while bits_per_weight() was used
    # elsewhere made Table 6 disagree with Table 2 on the same container.
    w = m["params"] * 1e9 * (bits_per_weight(model, fmt) / 8.0) / (1024**3)
    kv = kv_bytes_at_context(model, ctx, kv_bits) / (1024**3)
    return w, kv, w + kv + overhead_gb

def energy_per_token(tok_s, power_w):
    return power_w / tok_s if tok_s else float("nan")

def cost_from_energy(j_per_tok, tok_s, elec_usd_kwh=0.16, msrp=None,
                     amort_years=3.0, duty=0.25):
    """Cost per 1e6 tokens from a MEASURED energy figure.

    Preferred over cost_per_mtok() wherever a source reports joules per token
    directly: a measured J/token covers the whole inference window, whereas
    power/throughput recovers only the decode phase."""
    kwh_per_mtok = j_per_tok * 1e6 / 3.6e6
    elec = kwh_per_mtok * elec_usd_kwh
    if msrp is None:
        return elec, 0.0, elec
    tokens_life = tok_s * 3600 * 24 * 365 * amort_years * duty
    cap = msrp / (tokens_life / 1e6)
    return elec, cap, elec + cap

def cost_per_mtok(tok_s, power_w, elec_usd_kwh=0.16, msrp=None,
                  amort_years=3.0, duty=0.25):
    """Electricity + optional hardware amortization, USD per 1e6 tokens."""
    j_tok = energy_per_token(tok_s, power_w)
    kwh_per_mtok = j_tok * 1e6 / 3.6e6
    elec = kwh_per_mtok * elec_usd_kwh
    if msrp is None:
        return elec, 0.0, elec
    tokens_life = tok_s * 3600 * 24 * 365 * amort_years * duty
    cap = msrp / (tokens_life / 1e6)
    return elec, cap, elec + cap

if __name__ == "__main__":
    pd.set_option("display.width", 200)
    print("=== GPU SUBSTRATE ===")
    print(gpu.to_string(index=False))
    gpu.to_csv("/home/claude/review/t1_gpus.csv", index=False)
