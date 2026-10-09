"""
Table 2b -- the validity filter applied to measurements that CANNOT be normalized.

Why this file exists. The corpus in corpus.py is admitted under the inclusion
rule of Sec. V-A, which requires the batch or concurrency level to be stated in
the source. That rule makes the corpus, by construction, unable to contain the
mislabelled measurements the filter was built to catch: the three rows it flags
carry "batch 8" in their own column. Running the filter there is a check that it
agrees with ground truth, not a finding.

The filter's actual test set is the measurements Sec. V-B eliminated. For each,
we compute the RANGE of per-token traffic consistent with everything the source
states, then ask what the reported throughput implies at the batch-1 reading its
presentation invites. A measurement whose range straddles MBU = 1 cannot be
confirmed or refuted as batch-1 decoding from its own published description.
That is the filter returning "indeterminate", and it is a property of the
reporting, not of the hardware.

Nothing here claims a measurement is wrong. Each is a measurement whose
circulated label cannot be reconciled with its own numbers without information
the source withholds.

Every throughput figure below was read from its primary source in October 2026
and the verbatim sentence is recorded in verify/VERIFICATION_LOG.md. Every
architectural constant comes from the model's published config.json.
"""
import pandas as pd, numpy as np
from normalize import MODELS, BPW, gpu, kv_bytes_at_context

G = gpu.set_index("gpu").to_dict("index")

# --- Effective width of a partially quantized container ---------------------
# gpt-oss ships with quantization_config.quant_method = "mxfp4" and an explicit
# modules_to_not_convert list covering self_attn, the MoE router, embed_tokens and
# lm_head. The MoE weights are 4.25-bit; everything else stays BF16. A reader who
# treats the artifact as "4-bit" therefore understates its resident width. We
# derive the resident average from the config's own dimensions rather than
# assuming it.
GPT_OSS_CFG = {   # all fields read from the published config.json
  "gpt-oss-20b":  dict(total=21.0,  L=24, hid=2880, heads=64, hd=64, kvh=8,
                       experts=32,  vocab=201088, tied=False),
  "gpt-oss-120b": dict(total=117.0, L=36, hid=2880, heads=45, hd=64, kvh=8,
                       experts=128, vocab=201088, tied=False),
}
def gpt_oss_effective_bits(name, moe_bits=4.25, other_bits=16.0):
    """Resident average bits per weight, from the BF16 share the config pins."""
    c = GPT_OSS_CFG[name]
    qd, kvd = c["heads"]*c["hd"], c["kvh"]*c["hd"]
    attn = c["L"] * (c["hid"]*qd + 2*c["hid"]*kvd + qd*c["hid"])
    router = c["L"] * c["hid"] * c["experts"]
    embed = c["vocab"] * c["hid"] * (1 if c["tied"] else 2)
    other = (attn + router + embed) / 1e9          # billions, kept at BF16
    moe = c["total"] - other                        # the remainder is MXFP4
    return (moe*moe_bits + other*other_bits) / c["total"], other, moe

for n in GPT_OSS_CFG:
    b, o, m = gpt_oss_effective_bits(n)
    print(f"# {n}: {o:.2f}B BF16 + {m:.2f}B MXFP4 -> {b:.2f} effective bits/weight")

# --- Residency readings -----------------------------------------------------
# For a mixture-of-experts model, per-token weight traffic depends on a choice
# the sources never state: whether the reported rate reflects reading only the
# experts a token activates, or sweeping the resident weight set. Both appear in
# the literature. We bound rather than choose.
#
# For the containers, "low" is the nominal width of the format and "high" is the
# measured effective width of the widest container the source's label admits.
def w_bytes(model, bpw, use_active):
    m = MODELS[model]
    p = m["active"] if use_active else m["params"]
    return p * 1e9 * (bpw / 8.0)

CAND = [
 # ---- Source A: NVIDIA RTX AI Garage (corporate blog), gpt-oss launch -------
 dict(src="NVIDIA 2025a", gpu="RTX 5090", tok_s=256.0,
      label="gpt-oss, MXFP4", missing="model identity, batch, phase, seq. lengths, context",
      # The sentence gives "up to 256 tokens per second" for a paragraph that
      # discusses gpt-oss-20b and gpt-oss-120b together without attributing the
      # number to either. Both readings are therefore admissible.
      readings=[("20b, active path",  "gpt-oss-20b",  4.25, True,  4096),
                ("120b, active path", "gpt-oss-120b", 4.25, True,  4096),
                ("20b, resident sweep","gpt-oss-20b", gpt_oss_effective_bits("gpt-oss-20b")[0], False, 4096)],
      note="'expect performance of up to 256 tokens per second on the NVIDIA GeForce "
           "RTX 5090 GPU'; the paragraph names both gpt-oss-20b and gpt-oss-120b and "
           "attributes the figure to neither. MXFP4 covers the MoE weights only, so "
           "the config-implied resident average is well above the nominal 4.25"),

 # ---- Source B: TechRadar, sponsored content created with NVIDIA ------------
 dict(src="TechRadar 2025", gpu="RTX 5090", tok_s=282.0,
      label="gpt-oss-20b, no precision stated",
      missing="precision, batch, phase, seq. lengths, context",
      readings=[("active path, MXFP4", "gpt-oss-20b", 4.25, True,  4096),
                ("active path, BF16",  "gpt-oss-20b", 16.0, True,  4096),
                ("resident sweep, MXFP4","gpt-oss-20b", gpt_oss_effective_bits("gpt-oss-20b")[0], False, 4096)],
      note="'the GeForce RTX 5090 with 32GB of RAM, was able to run gpt-oss-20b in "
           "Llama.cpp at an impressive 282 tok/s'; same model and card as Source A, "
           "reported 10% higher, with no precision named on either page"),

 # ---- Source C: NVIDIA Developer Blog, llama.cpp on RTX ---------------------
 dict(src="NVIDIA 2024", gpu="RTX 4090", tok_s=150.0,
      label="Llama-3-8B, 'int4'", missing="batch, phase",
      readings=[("int4 nominal",      "Llama-3-8B", 4.25, False, 150),
                ("Q4_0 measured",     "Llama-3-8B", 4.64, False, 150),
                ("Q4_K_M measured",   "Llama-3-8B", 4.89, False, 150)],
      note="'users can expect ~150 tokens per second, with an input sequence length "
           "of 100 tokens and an output sequence length of 100 tokens'. Sequence "
           "lengths are stated, so C-bar is pinned at 150; batch and phase are not"),

 # ---- Source D: hardware-corner.net GPU ranking, 16k context ---------------
 *[dict(src="HW Corner 2025", gpu=g, tok_s=t,
        label="Qwen3-8B, Q4_K_XL", missing="batch, tokens generated, prompt length",
        readings=[("Q4_K_S measured", "Qwen3-8B", 4.67, False, 16384),
                  ("Q4_K_M measured", "Qwen3-8B", 4.89, False, 16384)],
        note=f"token-generation table at 16k context, 4-bit Q4_K_XL; batch size does "
             f"not appear anywhere on the page")
   for g, t in [("RTX 5090",145.34), ("RTX 4090",104.31), ("RTX 3090",87.45)]],

 *[dict(src="HW Corner 2025", gpu=g, tok_s=t,
        label="Qwen3-30B (A3B MoE), Q4_K_XL",
        missing="batch, expert residency, tokens generated, prompt length",
        readings=[("active path",    "Qwen3-30B-A3B", 4.67, True,  16384),
                  ("resident sweep", "Qwen3-30B-A3B", 4.89, False, 16384)],
        note=f"same table as the Qwen3-8B rows. The source writes 'Qwen3 30B' without "
             f"distinguishing total from active parameters, and the only 30B-class "
             f"Qwen3 is the A3B mixture of experts")
   for g, t in [("RTX 5090",141.63), ("RTX 4090",139.71), ("RTX 3090",113.84)]],
]

rows = []
for c in CAND:
    bw = G[c["gpu"]]["bw_gbs"] * 1e9
    recs = []
    for name, model, bpw, active, cbar in c["readings"]:
        b = w_bytes(model, bpw, active) + kv_bytes_at_context(model, cbar, 16)
        recs.append((name, b, c["tok_s"] * b / bw))
    lo = min(recs, key=lambda r: r[1]); hi = max(recs, key=lambda r: r[1])
    mbu_lo, mbu_hi = lo[2], hi[2]
    # The minimum concurrency that would reconcile the HIGH reading with the
    # device: how many streams must share one weight sweep for the traffic to fit.
    min_batch = int(np.ceil(mbu_hi)) if mbu_hi > 1 else None
    verdict = ("FLAGGED" if mbu_lo > 1 else
               "INDETERMINATE" if mbu_hi > 1 else "PASS")
    rows.append(dict(src=c["src"], gpu=c["gpu"], label=c["label"], tok_s=c["tok_s"],
        missing=c["missing"], b_lo=lo[1]/1e9, b_hi=hi[1]/1e9,
        read_lo=lo[0], read_hi=hi[0], mbu_lo=mbu_lo, mbu_hi=mbu_hi,
        span=hi[1]/lo[1], min_batch=min_batch, verdict=verdict, note=c["note"]))

df = pd.DataFrame(rows)
df.to_csv("/home/claude/review/t2b_candidates.csv", index=False)

pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
print("=== TABLE 2b: THE FILTER ON NON-NORMALIZABLE MEASUREMENTS ===\n")
print(df[["src","gpu","label","tok_s","b_lo","b_hi","span","mbu_lo","mbu_hi",
          "min_batch","verdict"]].round(2).to_string(index=False))

n = len(df)
print(f"\n--- summary over {n} measurements from {df.src.nunique()} sources ---")
for v in ["PASS","INDETERMINATE","FLAGGED"]:
    k = (df.verdict==v).sum()
    print(f"  {v:14s} {k}")
ind = df[df.verdict!="PASS"]
print(f"\n  {len(ind)} of {n} have an admissible reading under which the reported rate")
print(f"  exceeds the device's peak bandwidth at batch 1. None of the {n} can be")
print(f"  reduced to a common basis from its published description alone.")
print(f"\n  widest traffic ambiguity: {df.span.max():.1f}x ({df.loc[df.span.idxmax(),'label']})")
print(f"  narrowest:                {df.span.min():.2f}x ({df.loc[df.span.idxmin(),'label']})")
print(f"  median ambiguity:         {df.span.median():.2f}x")
print("\n--- the MoE pair, which the framework explains ---")
q = df[df.label.str.contains("A3B")]
print("  Qwen3-30B-A3B reported at nearly the same rate on cards 1.78x apart in")
print("  bandwidth: " + ", ".join(f"{r.gpu.replace('RTX ','')} {r.tok_s}" for r in q.itertuples()))
print("  Under the active-path reading the implied MBU is far below 1 on all three,")
print("  i.e. these runs are not bandwidth-bound, which is what makes a bandwidth")
print("  ranking of them uninformative. Under the resident-sweep reading they are")
print("  impossible. The source does not say which applies.")
