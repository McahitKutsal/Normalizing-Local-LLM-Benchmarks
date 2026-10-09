"""
VRAM feasibility frontier, computed from verified architectures.

Every model's layer count, KV-head count, head dimension and sliding-window
configuration was read from its published config.json (see VERIFICATION_LOG).
Effective bits per weight are the values derived in quality.py from published
container sizes, not assumed constants.
"""
import pandas as pd, numpy as np
from normalize import gpu, BPW, MODELS, vram_footprint, kv_bytes_at_context

FMTS   = ["FP16", "Q8_0", "Q6_K", "Q5_K_M", "Q4_K_M", "IQ3_M", "IQ2_M"]
CTXS   = [4096, 32768, 131072]
MODELS_F = ["Llama-3.1-8B", "Qwen3-8B", "Gemma-3-12B", "Gemma-3-27B",
            "Qwen2.5-32B", "Llama-3.3-70B"]
TIERS  = [8, 12, 16, 24, 32]

rec = []
for m in MODELS_F:
    for f in FMTS:
        for c in CTXS:
            w, kv, tot = vram_footprint(m, f, c)
            rec.append(dict(model=m, fmt=f, bpw=BPW[f], ctx=c, w_GiB=w,
                            kv_GiB=kv, total_GiB=tot, kv_share=100*kv/tot,
                            window=("sliding" if MODELS[m].get("win") else "full"),
                            min_tier=next((t for t in TIERS if tot <= t), None)))
fr = pd.DataFrame(rec)
fr.to_csv("/home/claude/review/t3_frontier.csv", index=False)

pd.set_option("display.width", 260); pd.set_option("display.max_columns", 50)
print("=== VRAM DEMAND (GiB): 4k / 32k / 128k context ===")
for f in ["Q4_K_M", "Q5_K_M"]:
    print(f"\n-- {f} --")
    sub = fr[fr.fmt == f].pivot(index="model", columns="ctx", values="total_GiB")
    sub = sub.reindex(MODELS_F)
    sub.columns = [f"{c//1024}k" for c in sub.columns]
    print(sub.round(1).to_string())

print("\n=== SMALLEST CONSUMER TIER THAT ADMITS EACH CONFIGURATION (GB) ===")
mt = fr[fr.ctx == 32768].pivot(index="model", columns="fmt", values="min_tier")
mt = mt.reindex(index=MODELS_F, columns=FMTS)
print("at 32k context:")
print(mt.to_string())

print("\n=== THE CONTEXT WALL, AND WHAT ARCHITECTURE DOES ABOUT IT ===")
print("KV cache as a share of total footprint at Q4_K_M:")
k = fr[fr.fmt == "Q4_K_M"].pivot_table(index=["model", "window"],
                                       columns="ctx", values="kv_share")
k.columns = [f"{c//1024}k" for c in k.columns]
print(k.round(1).to_string())
full = fr[(fr.fmt=="Q4_K_M") & (fr.ctx==32768) & (fr.window=="full")]
slid = fr[(fr.fmt=="Q4_K_M") & (fr.ctx==32768) & (fr.window=="sliding")]
print(f"\n  at 32k, full-attention models hold {full.kv_share.mean():.1f}% of their "
      f"footprint in cache (n={len(full)})")
print(f"  interleaved sliding-window models hold {slid.kv_share.mean():.1f}% (n={len(slid)})")
print(f"  -> the architectural fix is already deployed; it is the full-attention")
print(f"     models, not the largest ones, that pay the context wall")

print("\n=== EFFECT OF FP8 KV CACHE AT 32k ===")
for m in MODELS_F:
    _, k16, t16 = vram_footprint(m, "Q4_K_M", 32768, kv_bits=16)
    _, k8,  t8  = vram_footprint(m, "Q4_K_M", 32768, kv_bits=8)
    print(f"  {m:16s} {t16:6.2f} -> {t8:6.2f} GiB  (saves {t16-t8:5.2f}, {100*(t16-t8)/t16:4.1f}%)")

print("\n=== WHAT A 24 GB CARD ADMITS AT 32k ===")
ok24 = fr[(fr.ctx==32768) & (fr.total_GiB <= 24)]
for m in MODELS_F:
    s = ok24[ok24.model == m]
    best = s.nlargest(1, "bpw")
    if len(best):
        b = best.iloc[0]
        print(f"  {m:16s} highest-precision fit: {b.fmt:7s} ({b.bpw:.2f} bpw, {b.total_GiB:.1f} GiB)")
    else:
        print(f"  {m:16s} does not fit at any container considered")
