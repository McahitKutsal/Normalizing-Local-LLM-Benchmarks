"""
Quantization accuracy, from primary sources only.

Source A: unified llama.cpp evaluation on Llama-3.1-8B-Instruct (arXiv:2601.14277).
          WikiText-2 perplexity via llama.cpp's own get-wikitext-2.sh, plus five
          lm-evaluation-harness tasks (GSM8K 5-shot, HellaSwag acc_norm, IFEval,
          MMLU, TruthfulQA MC2). Baseline F16: avg 69.47, PPL 7.32.
Source B: the k-quants pull request that introduced the family
          (ggml-org/llama.cpp PR #1684), LLaMA-7B and LLaMA-13B, WikiText-2.

Effective bits per weight are DERIVED, not assumed: from the published size
reduction in Source A, and from the published file sizes in Source B.
"""
import pandas as pd, numpy as np
from normalize import roofline_tok_s, MODELS, BPW, kv_bytes_at_context

# ---- Source A: Llama-3.1-8B-Instruct, llama.cpp containers -------------
A = [   # quant, size_reduction_%, GSM8K, HSwag, IFEval, MMLU, TQA_mc2, avg, ppl
 ("F16",    0.00, 77.63, 72.51, 78.93, 63.50, 54.79, 69.47, 7.32),
 ("Q8_0",  46.87, 77.48, 72.52, 78.79, 63.43, 54.81, 69.41, 7.33),
 ("Q6_K",  58.98, 78.17, 72.48, 77.63, 63.17, 54.71, 69.23, 7.35),
 ("Q5_1",  62.27, 78.47, 72.08, 79.79, 63.68, 54.62, 69.73, 7.43),
 ("Q5_K_M",64.35, 78.54, 72.33, 78.67, 62.80, 54.45, 69.36, 7.40),
 ("Q5_0",  65.19, 79.08, 72.63, 80.14, 63.18, 54.57, 69.92, 7.43),
 ("Q5_K_S",65.19, 75.66, 72.67, 79.50, 63.36, 53.90, 69.02, 7.43),
 ("Q4_1",  68.11, 76.04, 71.29, 78.45, 63.17, 55.01, 68.79, 7.72),
 ("Q4_K_M",69.41, 77.41, 72.35, 79.06, 62.43, 54.49, 69.15, 7.56),
 ("Q4_K_S",70.83, 77.33, 72.79, 80.26, 62.06, 53.40, 69.17, 7.62),
 ("Q4_0",  71.03, 75.66, 71.88, 77.46, 62.20, 52.68, 67.98, 7.74),
 ("Q3_K_L",73.14, 74.07, 73.54, 79.14, 62.31, 54.84, 68.78, 7.81),
 ("Q3_K_M",75.03, 73.16, 73.41, 77.19, 62.01, 54.56, 68.07, 7.96),
 ("Q3_K_S",77.23, 68.31, 71.87, 73.89, 59.31, 54.08, 65.49, 8.96),
]
q = pd.DataFrame(A, columns=["quant","size_red","GSM8K","HSwag","IFEval",
                             "MMLU","TQA","avg","ppl"])
BASE_AVG, BASE_PPL = 69.47, 7.32
q["bpw"]        = 16.0 * (1 - q.size_red/100.0)      # derived from size reduction
q["compression"]= 16.0 / q.bpw
q["d_ppl"]      = q.ppl - BASE_PPL
q["d_avg_pp"]   = BASE_AVG - q.avg                   # positive = accuracy lost
q["d_gsm8k_pp"] = 77.63 - q.GSM8K                    # most precision-sensitive task

# Traffic-implied ceiling ratio on a reference RTX 4090 at mean cache occupancy
# 4096 (equation 3). This used to inline its own copy of the traffic formula,
# which then had to be kept in step with normalize.py by hand and was not: the
# inlined copy still halved the cache after equation (4) stopped doing so, which
# showed up as an F16 row whose ceiling ratio against itself was 1.02x rather
# than 1.00x. There is now one implementation.
REF_CBAR, REF_BW = 4096, 1008
def ceil_for(bpw):
    m = MODELS["Llama-3.1-8B"]
    w = m["params"]*1e9*(bpw/8.0)
    kv = kv_bytes_at_context("Llama-3.1-8B", REF_CBAR, 16)
    return (REF_BW*1e9)/(w+kv)
base = ceil_for(BPW["FP16"])
q["roofline"] = q.bpw.map(ceil_for)
q["speedup"]  = q.roofline/base
q["speedup_per_acc_pp"] = np.where(q.d_avg_pp > 0.05,
                                   (q.speedup-1)/q.d_avg_pp, np.nan)
q = q.sort_values("bpw", ascending=False).reset_index(drop=True)
q.to_csv("/home/claude/review/t4_quality.csv", index=False)

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
print("=== TABLE: ACCURACY vs COMPRESSION (Llama-3.1-8B-Instruct, arXiv:2601.14277) ===")
print(q[["quant","bpw","compression","ppl","d_ppl","avg","d_avg_pp",
         "d_gsm8k_pp","speedup"]].round(3).to_string(index=False))

print("\n--- where the trade actually turns ---")
for lo, hi, lbl in [(8.0, 16.1, ">= 8 bit"), (5.5, 8.0, "5.5-8 bit"),
                    (4.5, 5.5, "4.5-5.5 bit"), (4.0, 4.5, "4.0-4.5 bit"),
                    (0.0, 4.0, "< 4 bit")]:
    s = q[(q.bpw >= lo) & (q.bpw < hi) & (q.quant != "F16")]
    if len(s):
        print(f"  {lbl:12s} n={len(s)}  mean acc. loss {s.d_avg_pp.mean():+.2f} pp  "
              f"mean dPPL {s.d_ppl.mean():+.3f}  mean speedup {s.speedup.mean():.2f}x")

worst = q[q.quant=="Q3_K_S"].iloc[0]
q4 = q[q.quant=="Q4_K_M"].iloc[0]
q5 = q[q.quant=="Q5_K_M"].iloc[0]
print(f"\n  Q5_K_M  {q5.bpw:.2f} bpw: {q5.d_avg_pp:+.2f} pp, dPPL {q5.d_ppl:+.3f}, {q5.speedup:.2f}x")
print(f"  Q4_K_M  {q4.bpw:.2f} bpw: {q4.d_avg_pp:+.2f} pp, dPPL {q4.d_ppl:+.3f}, {q4.speedup:.2f}x")
print(f"  Q3_K_S  {worst.bpw:.2f} bpw: {worst.d_avg_pp:+.2f} pp, dPPL {worst.d_ppl:+.3f}, {worst.speedup:.2f}x")
print(f"  GSM8K alone falls {worst.d_gsm8k_pp:.2f} pp at Q3_K_S vs "
      f"{q4.d_gsm8k_pp:+.2f} pp at Q4_K_M -> reasoning degrades first")

# ---- Source B: independent cross-check on LLaMA-7B / 13B ---------------
B = [  # quant, size_7B_GB, ppl_7B, size_13B_GB, ppl_13B
 ("F16",   13.00, 5.9066, 25.00, 5.2543),
 ("Q6_K",   5.15, 5.9110,  9.95, 5.2568),
 ("Q5_K_M", 4.45, 5.9208,  8.60, 5.2638),
 ("Q5_K_S", 4.33, 5.9419,  8.36, 5.2785),
 ("Q4_K_M", 3.80, 5.9601,  7.32, 5.3002),
 ("Q4_K_S", 3.56, 6.0215,  6.80, 5.3404),
 ("Q3_K_L", 3.35, 6.0869,  6.45, 5.4063),
 ("Q3_K_M", 3.06, 6.1503,  5.88, 5.4498),
 ("Q3_K_S", 2.75, 6.4571,  5.27, 5.6033),
 ("Q2_K",   2.67, 6.7764,  5.13, 5.8545),
]
b = pd.DataFrame(B, columns=["quant","gb7","ppl7","gb13","ppl13"])
b["bpw7"]  = 16.0*b.gb7/13.00
b["bpw13"] = 16.0*b.gb13/25.00
b["d7"]    = b.ppl7 - 5.9066
b["d13"]   = b.ppl13 - 5.2543
b.to_csv("/home/claude/review/t4b_kquant.csv", index=False)
print("\n=== CROSS-CHECK: k-quant PR #1684, LLaMA-7B / 13B ===")
print(b[["quant","bpw7","d7","bpw13","d13"]].round(3).to_string(index=False))
agree = (b.bpw7 - b.bpw13).abs().max()
print(f"  bits-per-weight derived from 7B and 13B file sizes agree to "
      f"{agree:.2f} bits -> the derivation is stable")
j = q.merge(b, on="quant", how="inner")
print(f"  containers present in both sources: {len(j)}; "
      f"bpw correlation r = {np.corrcoef(j.bpw, j.bpw7)[0,1]:.4f}")
