"""
VERIFIED corpus. Every value below was read from its primary source in
September 2026 and is quoted in verify/VERIFICATION_LOG.md. Nothing here is
recalled or estimated. Rows whose throughput, container, batch size, context
or phase could not be confirmed were removed rather than filled in.
"""
import pandas as pd, numpy as np
from normalize import (gpu, BPW, bits_per_weight, MODELS, bytes_per_token, ctx_bar,
                       roofline_tok_s, cost_from_energy,
                       vram_footprint, energy_per_token, cost_per_mtok)

PCIE = {"PCIe 4.0 x16": 64.0, "PCIe 3.0 x16": 32.0}   # GB/s, vendor spec

# ---------------------------------------------------------------------
# A. Throughput measurements on consumer GPUs.
#
#    Context convention. Each row carries the prompt and generation lengths its
#    source states; mean cache occupancy C-bar = l_prompt + l_gen/2 is DERIVED by
#    ctx_bar(), and bytes_per_token() evaluates the cache at that depth without
#    halving again. Where a source does not report the split, `ctx_fixed` gives
#    C-bar directly and the note records what is assumed.
#
#    `phase` separates the numerator from the denominator of the reported rate,
#    which an earlier revision conflated:
#      "decode"       output tokens / decode-phase time. Directly comparable to a
#                     decode roofline.
#      "decode/total" output tokens / whole-request time. Prefill time sits in the
#                     denominator but its tokens are not in the numerator, so the
#                     rate UNDERSTATES decode speed and any resulting MBU is a
#                     lower bound -- the validity filter is conservative on these.
#      "mixed"        all tokens / whole-request time. Prefill tokens inflate the
#                     numerator; bias direction is bounded in Sec. VII-A.
#
#    spec FULL = throughput, container, batch, prompt/generation lengths and phase
#                all stated; PART = phase attribution ambiguous in the source.
#
#    REMOVED in the final verification pass: PowerInfer's OPT-30B measurement on
#    an RTX 4090. The paper reports that number only inside Fig. 10, whose caption
#    says "the number above each bar indicates the end-to-end generation speed",
#    and the figure is a raster image (_page_9_Figure_10.jpeg) in both the HTML
#    render and the PDF. No tokens-per-second figure for OPT-30B appears as text
#    anywhere in the paper. The value 16.06 that an earlier revision carried here
#    could not be traced to readable text and has been withdrawn. This is the same
#    disqualifier Sec. V-B applies to the Puget measurement, and applying it to one
#    source but not the other was an inconsistency. What the source does state as
#    text is kept in Sec. VII-C.
# ---------------------------------------------------------------------
REPORTED = [
 dict(study="Menlo 2024", gpu="RTX 4090", model="Mistral-7B", fmt="AWQ-4",
      engine="TensorRT-LLM", tok_s=170.63, l_prompt=2048, l_gen=512, batch=1,
      phase="mixed", spec="PART", resident=True,
      note="batch_size 1, ISL 2048 / OSL 512; Jan tokens/s spans prefill and decode"),
 dict(study="Menlo 2024", gpu="RTX 4090", model="Mistral-7B", fmt="Q4_K_M",
      engine="llama.cpp", tok_s=100.43, l_prompt=2048, l_gen=512, batch=1,
      phase="mixed", spec="PART", resident=True, note="as above"),
 dict(study="Menlo 2024", gpu="RTX 3090", model="Mistral-7B", fmt="AWQ-4",
      engine="TensorRT-LLM", tok_s=144.19, l_prompt=2048, l_gen=512, batch=1,
      phase="mixed", spec="PART", resident=True, note="as above"),
 dict(study="Menlo 2024", gpu="RTX 3090", model="Mistral-7B", fmt="Q4_K_M",
      engine="llama.cpp", tok_s=88.70, l_prompt=2048, l_gen=512, batch=1,
      phase="mixed", spec="PART", resident=True, note="as above"),
 dict(study="Zahl 2026", gpu="RTX 4060 Ti 16GB", model="Mistral-7B", fmt="Q4_K_M",
      engine="llama.cpp (Ollama)", tok_s=55.1, ctx_fixed=512, batch=1,
      phase="decode", spec="FULL", resident=True,
      note="decode-only via Ollama eval_count/eval_duration; the source gives no "
           "prompt/generation split, so C-bar=512 is assumed. Cache is 1.5% of this "
           "row's traffic, so the assumption moves B_tok by under 1%"),
 dict(study="Knoop 2026", gpu="RTX 5090", model="Qwen3-8B", fmt="NVFP4",
      engine="vLLM", tok_s=411.0, l_prompt=8192, l_gen=512, batch=8,
      phase="decode/total", spec="FULL", resident=True,
      note="RAG-8k tier, ISL 8192 / OSL 512, concurrency 8; metric is 'total output "
           "tokens per second (global TPS)', so output tokens over a window that "
           "includes the 8192-token prefill. TTFT 450 ms is reported separately"),
 dict(study="Knoop 2026", gpu="RTX 5070 Ti", model="Qwen3-8B", fmt="NVFP4",
      engine="vLLM", tok_s=211.0, l_prompt=8192, l_gen=512, batch=8,
      phase="decode/total", spec="FULL", resident=True, note="as above, concurrency 8"),
 dict(study="Knoop 2026", gpu="RTX 5060 Ti 16GB", model="Qwen3-8B", fmt="NVFP4",
      engine="vLLM", tok_s=115.0, l_prompt=8192, l_gen=512, batch=8,
      phase="decode/total", spec="FULL", resident=True, note="as above, concurrency 8"),
]

# ---------------------------------------------------------------------
# B. Directly measured energy. No architectural assumption enters these.
#    Zahl & Hennig 2026, Table III: RTX 4060 Ti 16GB, Ollama, decode-only, batch 1.
# ---------------------------------------------------------------------
ENERGY = [
 ("gemma3:1b",     207.7, 0.556,  83.26),
 ("llama3.2:1b",   173.0, 0.647,  82.31),
 ("gemma4:e2b",    114.0, 1.093, 108.71),
 ("llama3.2:3b",   112.4, 1.225, 101.82),
 ("qwen3.5:2b",     91.3, 1.221, 103.68),
 ("qwen2.5:3b",    107.8, 1.252, 106.02),
 ("phi4-mini:3.8b", 86.5, 1.595, 115.54),
 ("gemma3:4b",      78.5, 1.671, 110.25),
 ("mistral:7b",     55.1, 2.485, 122.50),
]

gmap = gpu.set_index("gpu").to_dict("index")
rows = []
for r in REPORTED:
    gi = gmap[r["gpu"]]
    # Mean cache occupancy. The averaging over the generation happens HERE and
    # nowhere else; bytes_per_token() must not halve again (see normalize.ctx_bar).
    cbar = r["ctx_fixed"] if "ctx_fixed" in r else ctx_bar(r["l_prompt"], r["l_gen"])
    model, fmt = r["model"], r["fmt"]
    w, kv, bpt = bytes_per_token(model, fmt, cbar, 16, True)
    ceil_vram = roofline_tok_s(model, fmt, gi["bw_gbs"], cbar, 16, True)
    ceil_pcie = (PCIE["PCIe 4.0 x16"] * 1e9) / bpt          # naive full-stream bound
    _, _, vtot = vram_footprint(model, fmt, cbar)
    rows.append(dict(study=r["study"], gpu=r["gpu"], arch=gi["arch"], model=model,
        fmt=fmt, engine=r["engine"], ctx=cbar,
        l_prompt=r.get("l_prompt"), l_gen=r.get("l_gen"),
        batch=r["batch"], phase=r["phase"], spec=r["spec"], tok_s=r["tok_s"],
        bpw=bits_per_weight(model, fmt), w_tok_GB=w/1e9, kv_tok_GB=kv/1e9,
        bytes_tok_GB=bpt/1e9,
        bw_gbs=gi["bw_gbs"], roofline_vram=ceil_vram, roofline_pcie=ceil_pcie,
        MBU=r["tok_s"]/ceil_vram, tok_s_per_TBs=r["tok_s"]/(gi["bw_gbs"]/1000.0),
        vram_need=vtot, vram_have=gi["vram_gb"],
        regime=("resident" if r["resident"] else "offloaded"),
        exceeds_b1=(r["tok_s"]/ceil_vram > 1.0), note=r["note"]))

df = pd.DataFrame(rows)
df.to_csv("/home/claude/review/t2_normalized.csv", index=False)

en = pd.DataFrame(ENERGY, columns=["model","tok_s","J_per_tok","mean_W"])
en.to_csv("/home/claude/review/t5_energy.csv", index=False)

pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
print("=== VERIFIED CORPUS ===")
print(df[["study","gpu","model","fmt","engine","ctx","batch","phase","spec",
          "tok_s","bytes_tok_GB","roofline_vram","MBU","regime"]].round(3).to_string(index=False))

print("\n=== [F1] BATCH-1 CEILING CHECK ===")
over = df[df.exceeds_b1]
print(f"Rows above the batch-1 VRAM roofline: {len(over)} of {len(df)}")
print(over[["study","gpu","model","tok_s","roofline_vram","MBU","batch"]].round(2).to_string(index=False))
print("All flagged rows are independently documented by their source as batched.")
print("The filter therefore recovers a fact the reported number alone does not carry.")

print("\n=== [F2] ENGINE EFFECT ON MATCHED HARDWARE AND MODEL (Menlo 2024) ===")
m = df[df.study=="Menlo 2024"]
for g in ["RTX 4090","RTX 3090"]:
    s = m[m.gpu==g]
    t = s[s.engine=="TensorRT-LLM"].iloc[0]; l = s[s.engine=="llama.cpp"].iloc[0]
    print(f"  {g}: raw {t.tok_s:6.2f} / {l.tok_s:6.2f} = {t.tok_s/l.tok_s:.2f}x   "
          f"MBU {t.MBU:.3f} / {l.MBU:.3f} = {t.MBU/l.MBU:.2f}x   "
          f"(bpw {t.bpw:.2f} vs {l.bpw:.2f})")
raw = m[m.engine=="TensorRT-LLM"].tok_s.mean()/m[m.engine=="llama.cpp"].tok_s.mean()
nor = m[m.engine=="TensorRT-LLM"].MBU.mean()/m[m.engine=="llama.cpp"].MBU.mean()
print(f"  pooled raw {raw:.2f}x -> normalized {nor:.2f}x; normalization accounts for "
      f"{100*(raw-nor)/(raw-1):.0f}% of the apparent gap, {100*(nor-1)/(raw-1):.0f}% survives")

print("\n=== [F3] OFFLOADED EXECUTION ===")
off = df[df.regime=="offloaded"]
if off.empty:
    print("  No offloaded measurement survives verification. The candidate (PowerInfer,")
    print("  OPT-30B FP16 on an RTX 4090) reports its throughput only inside a figure")
    print("  image, so it fails the same inclusion rule that excluded Puget. Sec. VII-C")
    print("  now rests on what that source states as text, and reports no MBU for it.")
else:
    for _, r in off.iterrows():
        print(f"  {r.study}: {r.model} {r.fmt} on {r.gpu}, {r.tok_s} tok/s")
        print(f"    naive PCIe 4.0 bound   : {r.roofline_pcie:6.2f} tok/s  "
              f"-> achieved {r.tok_s/r.roofline_pcie:5.1f}x the naive bound")
        print(f"    hypothetical resident  : {r.roofline_vram:6.2f} tok/s  "
              f"-> achieved {100*r.tok_s/r.roofline_vram:5.1f}% of it")

print("\n=== [F4] MEASURED ENERGY (Zahl & Hennig 2026, RTX 4060 Ti) ===")
print(en.round(3).to_string(index=False))
print(f"  J/token spans {en.J_per_tok.min():.3f}-{en.J_per_tok.max():.3f} "
      f"({en.J_per_tok.max()/en.J_per_tok.min():.1f}x) across 1B-7B")
print(f"  corr(throughput, J/token) = {np.corrcoef(en.tok_s, en.J_per_tok)[0,1]:.3f}")

print("\n=== [F5] COST PER MILLION TOKENS, FROM MEASURED ENERGY ===")
msrp = gmap["RTX 4060 Ti 16GB"]["msrp_usd"]
cst = []
for _, r in en.iterrows():
    # Electricity from the measured J/token, which covers the full inference
    # window. Using mean_W / tok/s instead would silently drop prefill energy.
    e, c, tot = cost_from_energy(r.J_per_tok, r.tok_s, msrp=msrp)
    cst.append((r.model, r.tok_s, e, c, tot))
cd = pd.DataFrame(cst, columns=["model","tok_s","USD_elec","USD_amort","USD_total"])
print(cd.round(3).to_string(index=False))
share = 100*cd.USD_elec.sum()/cd.USD_total.sum()
under = cd.USD_total.sum()/cd.USD_elec.sum()
print(f"  electricity share of true cost: {share:.1f}%")
print(f"  electricity-only accounting understates cost by {under:.1f}x "
      f"at a 25% duty cycle")

# How much of the measured energy is prefill plus call overhead: the gap
# between the source's window-wide J/token and the decode-only ratio.
en["J_decode_only"] = en.mean_W / en.tok_s
en["J_overhead"]    = en.J_per_tok - en.J_decode_only
print(f"\n  measured J/token covers the whole inference window; the decode-only")
print(f"  ratio mean_W/(tok/s) is lower by {en.J_overhead.min():.3f}-"
      f"{en.J_overhead.max():.3f} J ({100*(en.J_overhead/en.J_per_tok).mean():.0f}% of the total")
print(f"  on average), which is the prefill and call-overhead share. Eq. (6) is")
print(f"  therefore a decode-only approximation, not an identity on this table.")
cd.to_csv("/home/claude/review/t6_cost.csv", index=False)
