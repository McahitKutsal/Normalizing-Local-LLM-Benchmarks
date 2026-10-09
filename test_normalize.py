"""Regression tests for the normalization core.

Run: python3 test_normalize.py

Each test recomputes a tabulated value from architectural constants by hand, so a
change in normalize.py that alters a published number fails here rather than
silently shipping. test_btok_mistral_menlo and test_no_double_averaging exist
because an earlier revision averaged the cache over the generation twice.
"""
import sys
from normalize import (MODELS, bits_per_weight, bytes_per_token, ctx_bar,
                       kv_bytes_at_context, roofline_tok_s, gpu)

FAIL = []
def check(name, got, want, tol):
    if isinstance(want, bool):
        ok = bool(got) == want
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {bool(got)}, want {want}")
        if not ok: FAIL.append(name)
        return
    got, want = float(got), float(want)
    ok = abs(got - want) <= tol
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: got {got:.6g}, want {want:.6g} (+-{tol:g})")
    if not ok: FAIL.append(name)

def test_ctx_bar():
    """C-bar is prompt plus HALF the generation -- the only averaging step."""
    check("ctx_bar(2048,512)", ctx_bar(2048, 512), 2304, 0)
    check("ctx_bar(8192,512)", ctx_bar(8192, 512), 8448, 0)
    check("ctx_bar(64,512)",   ctx_bar(64, 512),    320, 0)

def test_kv_per_token_mistral():
    """2 tensors x 8 KV heads x 128 head_dim x 2 B x 32 layers = 131072 B/token."""
    check("Mistral-7B KV bytes per token of depth",
          kv_bytes_at_context("Mistral-7B", 1, 16), 2*8*128*2*32, 0)

def test_btok_mistral_menlo():
    """The Menlo rows, hand-computed from first principles.

    AWQ-4 weights: measured artifact 4.150e9 B (TheBloke Mistral-7B-Instruct-v0.2-AWQ)
    Cache at C-bar = 2048 + 512/2 = 2304: 131072 * 2304 = 0.3020e9 B
    B_tok = 4.452 GB.  NOT 4.305 GB, which is what halving a C-bar that is
    already a mean produces.
    """
    cbar = ctx_bar(2048, 512)
    w, kv, bpt = bytes_per_token("Mistral-7B", "AWQ-4", cbar)
    check("Menlo AWQ-4 B_w  (GB)",   w/1e9,   4.1500, 0.002)
    check("Menlo AWQ-4 B_kv (GB)",   kv/1e9,  0.30199, 0.0005)
    check("Menlo AWQ-4 B_tok (GB)",  bpt/1e9, 4.4520, 0.002)
    check("Menlo AWQ-4 B_tok is NOT the double-averaged 4.305 GB",
          abs(bpt/1e9 - 4.305) > 0.1, True, 0)
    w2, kv2, bpt2 = bytes_per_token("Mistral-7B", "Q4_K_M", cbar)
    check("Menlo Q4_K_M B_tok (GB)", bpt2/1e9, 4.6720, 0.002)
    bw = gpu.set_index("gpu").loc["RTX 4090", "bw_gbs"]
    check("RTX 4090 vendor peak bandwidth (GB/s)", bw, 1008.0, 0.5)
    check("Menlo 4090 AWQ-4 ceiling (tok/s)",
          roofline_tok_s("Mistral-7B", "AWQ-4", bw, cbar), 226.2, 1.0)
    check("Menlo 4090 AWQ-4 MBU", 170.63/roofline_tok_s("Mistral-7B","AWQ-4",bw,cbar),
          0.754, 0.003)

def test_btok_knoop():
    """Knoop rows: ISL 8192 / OSL 512 -> C-bar = 8448, verified from the source."""
    cbar = ctx_bar(8192, 512)
    w, kv, bpt = bytes_per_token("Qwen3-8B", "NVFP4", cbar)
    check("Qwen3-8B KV bytes per token of depth",
          kv_bytes_at_context("Qwen3-8B", 1, 16), 2*8*128*2*36, 0)
    check("Knoop B_tok (GB)", bpt/1e9, 5.853, 0.01)
    bw = gpu.set_index("gpu").loc["RTX 5090", "bw_gbs"]
    check("Knoop 5090 MBU exceeds 1 (filter fires)",
          411.0/roofline_tok_s("Qwen3-8B","NVFP4",bw,cbar) > 1.0, True, 0)

def test_no_double_averaging():
    """B_tok must be linear in C-bar with slope = full per-token cache bytes.

    If any halving survived anywhere, the recovered slope would be half this."""
    m = "Mistral-7B"
    _, _, b1 = bytes_per_token(m, "Q4_K_M", 1000)
    _, _, b2 = bytes_per_token(m, "Q4_K_M", 2000)
    slope = (b2 - b1) / 1000.0
    check("d(B_tok)/d(C-bar) equals full per-token cache bytes",
          slope, 2*8*128*2*32, 1.0)

def test_sliding_window_is_not_regressed():
    """Gemma 3 keeps 1 global layer per 6; above the window the cache stops
    growing linearly. Guards the fix from the previous revision round."""
    g = "Gemma-3-12B"
    if g not in MODELS:
        print(f"  SKIP  {g} absent from registry"); return
    m = MODELS[g]
    check(f"{g} declares a sliding window", bool(m.get("win")), True, 0)
    far = kv_bytes_at_context(g, 32768, 16)
    naive = 2*m["kvh"]*m["hd"]*2*m["L"]*32768
    check(f"{g} windowed cache at 32k is far below the full-attention value",
          far < naive/3, True, 0)

for t in [test_ctx_bar, test_kv_per_token_mistral, test_btok_mistral_menlo,
          test_btok_knoop, test_no_double_averaging,
          test_sliding_window_is_not_regressed]:
    print(f"\n{t.__name__}:"); t()
print("\n" + ("ALL TESTS PASSED" if not FAIL else f"{len(FAIL)} FAILED: {FAIL}"))
sys.exit(1 if FAIL else 0)
