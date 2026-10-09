#!/usr/bin/env python3
"""Generate paper/tables.json from the analysis CSVs.

Every numeric cell in the manuscript's tables is produced here from the output of
normalize.py / corpus.py / quality.py / frontier.py. Nothing is typed by hand.
Before this script existed, tables.json was maintained manually, and a change to
the corpus did not reach the manuscript -- the failure mode that let a stale
Table 2 survive a correction to equation (4).

Run order:  python3 corpus.py && python3 quality.py && python3 frontier.py \
            && python3 gen_tables.py

t4 (kernel and algorithmic mechanisms) is qualitative prose traced to sources and
has no derived cells, so it is carried through from the existing file unchanged.
"""
import json, pandas as pd, pathlib

R = pathlib.Path("/home/claude/review")
OUT = R / "paper" / "tables.json"
prev = json.loads(OUT.read_text()) if OUT.exists() else {}
T = {}

def s(x, n):   return f"{float(x):.{n}f}"
def sx(x, n):  return f"{float(x):.{n}f}×"
def sg(x, n):  return f"{float(x):+.{n}f}"

# ---- t1: hardware substrate -------------------------------------------------
g = pd.read_csv(R/"t1_gpus.csv").sort_values("bw_per_dollar", ascending=False)
T["t1"] = [["GPU","Arch.","VRAM (GB)","BW (GB/s)","TDP (W)","MSRP (USD)",
            "GB/s / USD","GB/s / W"]] + [
    [r.gpu.replace("RTX ","RTX ").replace(" 16GB","16G").replace(" 12GB","12G"),
     r.arch, str(int(r.vram_gb)), str(int(r.bw_gbs)), str(int(r.tdp_w)),
     str(int(r.msrp_usd)), s(r.bw_per_dollar,2), s(r.bw_per_watt,2)]
    for r in g.itertuples()]

# ---- t2: quantization containers (paper Table 3) ----------------------------
# Column names are direction-neutral: both increase columns are "cost" columns,
# so a reader never has to infer a sign convention. See Sec. VI-B.
q = pd.read_csv(R/"t4_quality.csv")
# Uncertainty column: the conservative end of the paired sampling bound for the
# GSM8K column (15% discordance on n=1319), with a dagger on the rows that also
# clear the attribution floor set by the Q5_0 / Q5_K_S pair. See uncertainty.py.
unc = pd.read_csv(R/"t_uncertainty.csv").set_index("quant")
def sig_cell(name):
    if name not in unc.index: return "n/a"
    r = unc.loc[name]
    return f"{r.sigma_lo:.1f}" + ("\u2020" if r.verdict == "ROBUST" else "")
T["t2"] = [["Container","Eff. bits/wt","Compr.","PPL","PPL incr.","5-task mean",
            "Acc. loss (pp)","GSM8K loss (pp)","GSM8K \u03c3","Roofline"]] + [
    # Signs are shown explicitly: all three delta columns are COST columns
    # (positive = worse), so a negative entry marks a container that scored
    # above the F16 baseline on that metric -- which Sec. VI-B reads as noise,
    # not as an improvement.
    [r.quant, s(r.bpw,2), sx(r.compression,2), s(r.ppl,2), sg(r.d_ppl,2),
     s(r.avg,2), sg(r.d_avg_pp,2), sg(r.d_gsm8k_pp,2), sig_cell(r.quant),
     sx(r.speedup,2)]
    for r in q.itertuples()]

# ---- t4: VRAM feasibility frontier (paper Table 5) --------------------------
fr = pd.read_csv(R/"t3_frontier.csv")
f32 = fr[fr.ctx == 32768]
fmts = ["FP16","Q8_0","Q6_K","Q5_K_M","Q4_K_M","IQ3_M","IQ2_M"]
models = [m for m in dict.fromkeys(f32.model) ]
T["t4"] = [["Model","Attn."] + fmts] + [
    [m, f32[f32.model==m].iloc[0].window] +
    [str(int(round(f32[(f32.model==m)&(f32.fmt==x)].iloc[0].total_GiB)))
     if len(f32[(f32.model==m)&(f32.fmt==x)]) else "--" for x in fmts]
    for m in models]

# ---- t5: the verified corpus (paper Table 2) --------------------------------
c = pd.read_csv(R/"t2_normalized.csv")
# Every surviving row is VRAM-resident, so the MBU column holds one quantity
# throughout. The offloaded candidate that used to need a column of its own was
# withdrawn: its throughput appears only inside a figure image in its source.
def mbu_cell(r):
    return s(r.MBU,2) + ("*" if r.exceeds_b1 else "")
T["t5"] = [["Study","GPU (RTX)","Model","Container","Engine","Ctx","Batch","Phase",
            "tok/s","B_tok (GB)","Ceiling","MBU"]] + [
    [r.study, r.gpu.replace("RTX ",""), r.model, r.fmt, r.engine,
     str(int(r.ctx)), str(int(r.batch)), r.phase, s(r.tok_s,1),
     s(r.bytes_tok_GB,2) + ("†" if r.regime=="offloaded" else ""),
     str(int(round(r.roofline_vram))), mbu_cell(r)]
    for r in c.itertuples()]

# ---- t6: measured energy and derived cost (paper Table 6) -------------------
en = pd.read_csv(R/"t5_energy.csv"); cs = pd.read_csv(R/"t6_cost.csv")
m = en.merge(cs[["model","USD_elec","USD_amort","USD_total"]], on="model")
T["t6"] = [["Model (Ollama tag)","tok/s","J / token","Mean W","USD/MTok elec.",
            "USD/MTok amort.","USD/MTok total"]] + [
    [r.model, s(r.tok_s,1), s(r.J_per_tok,3), s(r.mean_W,1),
     s(r.USD_elec,3), s(r.USD_amort,3), s(r.USD_total,3)]
    for r in m.itertuples()]

# ---- t7: non-normalizable candidates (paper Table 3) ------------------------
cd = pd.read_csv(R/"t2b_candidates.csv")
def rng(a, b, n=2):
    return s(a,n) if abs(a-b) < 10**(-n) else f"{s(a,n)}–{s(b,n)}"
T["t7"] = [["Source","GPU (RTX)","Model and container as stated","Unstated field(s)",
            "tok/s","B_tok range (GB)","MBU at batch 1","Min. batch","Verdict"]] + [
    [r.src, r.gpu.replace("RTX ",""), r.label, r.missing, s(r.tok_s,1),
     rng(r.b_lo, r.b_hi), rng(r.mbu_lo, r.mbu_hi),
     ("n/a" if pd.isna(r.min_batch) else str(int(r.min_batch))), r.verdict]
    for r in cd.itertuples()]

# ---- t3: qualitative, carried through -----------------------------------
if "t3" in prev:
    T["t3"] = prev["t3"]
else:
    raise SystemExit("t3 (mechanism table) missing and cannot be derived")

order = ["t1","t2","t3","t4","t5","t6","t7"]
OUT.write_text(json.dumps({k: T[k] for k in order}, ensure_ascii=False, indent=1))
print(f"wrote {OUT}")
for k in order:
    print(f"  {k}: {len(T[k])-1} data rows x {len(T[k][0])} cols")
print("\nTable 2 (corpus) as it will appear:")
for row in T["t5"]:
    print("  " + " | ".join(f"{c:>12s}" for c in row))
