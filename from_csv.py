#!/usr/bin/env python3
"""
normalize --from-csv : turn the Sec. XI reporting standard from a checklist into
a tool. A reader writes their own measurement into a CSV using the Sec. XI field
names and gets MBU, the ceiling and the filter verdict back.

    python3 from_csv.py --from-csv measurements.csv
    python3 from_csv.py --template > my_measurements.csv
    python3 from_csv.py --reproduce-table2

A missing field does not fail silently. Each equation declares which columns it
consumes, and anything that cannot be computed is reported by name together with
the equation that needed it, so the output says what the measurement is missing
rather than guessing a default. Guessing defaults is the practice this paper
exists to argue against.
"""
import argparse, csv, sys, math
from normalize import (MODELS, BPW, bits_per_weight, bytes_per_token, ctx_bar,
                       kv_bytes_at_context, roofline_tok_s, gpu)

# column -> (required by, human description).  These names ARE the Sec. XI list.
FIELDS = {
 "model":        ("eq 1", "model identifier; must be in the registry or give params/active"),
 "params_b":     ("eq 1", "total parameters in billions (optional if model is known)"),
 "active_b":     ("eq 1", "activated parameters per token, billions (= params_b if dense)"),
 "container":    ("eq 1", "quantization container, e.g. Q4_K_M, AWQ-4, NVFP4"),
 "bits_per_weight":("eq 1","effective bits per weight MEASURED from artifact size; "
                           "blank falls back to the generic table and is flagged"),
 "kv_bits":      ("eq 2", "key-value cache precision in bits, usually 16 or 8"),
 "layers":       ("eq 2", "number of layers (optional if model is known)"),
 "kv_heads":     ("eq 2", "key-value heads (optional if model is known)"),
 "head_dim":     ("eq 2", "head dimension (optional if model is known)"),
 "sliding_window":("eq 2","sliding-window span in tokens; blank means full attention"),
 "window_pattern":("eq 2","layers per full-attention layer; blank means 1"),
 "prompt_tokens":("eq 3", "prompt length L_p"),
 "generated_tokens":("eq 3","tokens generated L_g"),
 "gpu":          ("eq 5", "device name; must be in the registry or give bandwidth_gbs"),
 "bandwidth_gbs":("eq 5", "peak memory bandwidth in GB/s (optional if gpu is known)"),
 "tok_s":        ("eq 6", "the reported throughput"),
 "batch":        ("eq 6", "batch size or concurrency level"),
 "phase":        ("eq 6", "decode | decode/total | mixed | prefill"),
 "resident":     ("eq 5", "yes if the working set was fully VRAM-resident"),
 "speculative":  ("Sec. IV-G", "yes/no; acceptance rate in the next column if yes"),
 "spec_accept":  ("Sec. IV-G", "mean accepted tokens per verification step"),
 "power_w":      ("eq 7", "sustained board power, if energy is reported"),
 "energy_j_tok": ("eq 7", "measured joules per token, if reported"),
 "energy_window":("eq 7", "what the energy integration covers: decode | whole-call"),
}
NUM = {"params_b","active_b","bits_per_weight","kv_bits","layers","kv_heads","head_dim",
       "sliding_window","window_pattern","prompt_tokens","generated_tokens",
       "bandwidth_gbs","tok_s","batch","power_w","energy_j_tok","spec_accept"}

def num(row, key):
    v = (row.get(key) or "").strip()
    if v == "": return None
    try: return float(v)
    except ValueError: raise SystemExit(f"row {row.get('_n')}: {key}={v!r} is not a number")

def evaluate(row):
    miss, warn = [], []
    model = (row.get("model") or "").strip()
    reg = MODELS.get(model)

    def arch(field, col):
        v = num(row, col)
        if v is not None: return v
        if reg and field in reg and reg[field] is not None: return reg[field]
        if reg and field in reg: return None          # legitimately None (no window)
        miss.append((col, FIELDS[col][0])); return None

    params = num(row,"params_b")  or (reg["params"] if reg else None)
    active = num(row,"active_b")  or (reg["active"] if reg else params)
    if params is None: miss.append(("params_b", "eq 1"))
    L   = arch("L","layers"); kvh = arch("kvh","kv_heads"); hd = arch("hd","head_dim")
    win = num(row,"sliding_window") or (reg.get("win") if reg else None)
    pat = num(row,"window_pattern") or (reg.get("pat") if reg else 1) or 1

    cont = (row.get("container") or "").strip()
    bpw  = num(row,"bits_per_weight")
    if bpw is None:
        if model and cont and (model, cont) in getattr(__import__("normalize"),"BPW_MEASURED",{}):
            bpw = bits_per_weight(model, cont)
        elif cont in BPW:
            bpw = BPW[cont]
            warn.append(f"bits_per_weight not given; used the generic value for "
                        f"{cont} ({bpw:.2f}). Sec. VI-A: measure the artifact instead")
        else:
            miss.append(("bits_per_weight", "eq 1"))

    kvb = num(row,"kv_bits")
    if kvb is None: miss.append(("kv_bits","eq 2"))
    lp, lg = num(row,"prompt_tokens"), num(row,"generated_tokens")
    if lp is None: miss.append(("prompt_tokens","eq 3"))
    if lg is None: miss.append(("generated_tokens","eq 3"))

    bw = num(row,"bandwidth_gbs")
    if bw is None:
        g = gpu.set_index("gpu")
        name = (row.get("gpu") or "").strip()
        if name in g.index: bw = float(g.loc[name,"bw_gbs"])
        else: miss.append(("bandwidth_gbs","eq 5"))

    t  = num(row,"tok_s");  b = num(row,"batch")
    if t is None: miss.append(("tok_s","eq 6"))
    if b is None: miss.append(("batch","eq 6"))
    phase = (row.get("phase") or "").strip().lower()
    if phase not in {"decode","decode/total","mixed","prefill"}:
        miss.append(("phase","eq 6"))

    out = {"missing": miss, "warnings": warn}
    if miss: return out

    cbar = ctx_bar(lp, lg)
    per_layer = 2 * kvh * hd * (kvb/8.0)
    if win:
        n_full = max(1, round(L/pat)); n_local = L - n_full
        kv = per_layer * (n_full*cbar + n_local*min(cbar, win))
    else:
        kv = per_layer * L * cbar
    w = active * 1e9 * (bpw/8.0)
    btok = w + kv
    ceil = (bw*1e9)/btok
    mbu  = t * btok / (bw*1e9)

    # The same number gets two verdicts, which is the point of Sec. V-D: what the
    # filter says when the batch is stated, and what it would say to a reader who
    # met the figure presented as single-stream.
    as_b1 = "FLAGGED" if mbu > 1.0 else "PASS"
    out["as_batch1"] = as_b1
    out["min_batch"] = math.ceil(mbu) if mbu > 1.0 else None
    verdict, note = "PASS", ""
    if phase == "prefill":
        verdict, note = "N/A", "prefill is compute-bound; the decode ceiling does not apply"
    elif mbu > 1.0:
        if b and b > 1:
            verdict = "PASS (batched)"
            note = (f"MBU {mbu:.2f} exceeds 1 but batch is {b:.0f}; the aggregate ceiling "
                    f"is {(bw*1e9)/(w/b + kv):.0f} tok/s and the figure is consistent with it"
                    if t <= (bw*1e9)/(w/b + kv) else
                    f"MBU {mbu:.2f} exceeds the ceiling even at batch {b:.0f}")
            if t > (bw*1e9)/(w/b + kv): verdict = "FLAGGED"
        else:
            verdict = "FLAGGED"
            note = f"minimum batch that reconciles this: {math.ceil(mbu)}"
    if (row.get("speculative") or "").strip().lower() in {"yes","true","1"}:
        note += ("; speculative decoding breaks the one-sweep-one-token premise of eq (4), "
                 "so the ceiling does not bind -- see Sec. IV-G")
    out.update(btok_gb=btok/1e9, w_gb=w/1e9, kv_gb=kv/1e9, cbar=cbar,
               ceiling=ceil, mbu=mbu, verdict=verdict, note=note)
    ej = num(row,"energy_j_tok"); pw = num(row,"power_w")
    if ej is not None:
        out["j_per_tok"] = ej
        out["energy_note"] = ("whole-call window: includes prefill"
            if (row.get("energy_window") or "").strip().startswith("whole")
            else "decode window" )
    elif pw is not None and t:
        out["j_per_tok"] = pw/t
        out["energy_note"] = "derived by eq (7) from sustained power; decode only"
    return out

def run(path):
    bad = 0
    with open(path, newline="") as f:
        for n, row in enumerate(csv.DictReader(f), start=2):
            row["_n"] = n
            name = " / ".join(x for x in [(row.get("gpu") or "").strip(),
                                          (row.get("model") or "").strip(),
                                          (row.get("container") or "").strip()] if x)
            r = evaluate(row)
            print(f"\n--- row {n}: {name or '(unnamed)'}")
            for w in r["warnings"]: print(f"    WARNING  {w}")
            if r["missing"]:
                bad += 1
                print("    CANNOT NORMALIZE. Missing field(s), with the equation each blocks:")
                for col, eq in r["missing"]:
                    print(f"      {col:20s} needed by {eq:10s} -- {FIELDS[col][1]}")
                continue
            print(f"    C-bar {r['cbar']:.0f} tokens    B_w {r['w_gb']:.3f} GB + "
                  f"B_kv {r['kv_gb']:.3f} GB = B_tok {r['btok_gb']:.3f} GB")
            print(f"    ceiling at batch 1 {r['ceiling']:.1f} tok/s    MBU {r['mbu']:.3f}")
            if "j_per_tok" in r:
                print(f"    energy {r['j_per_tok']:.3f} J/token ({r['energy_note']})")
            print(f"    {r['verdict']}" + (f"  -- {r['note']}" if r["note"] else ""))
            if r.get("as_batch1") == "FLAGGED":
                print(f"    AS PRESENTED AT BATCH 1 this figure would be FLAGGED "
                      f"(min batch {r['min_batch']}). If it travels without its batch "
                      f"size, that is the verdict a reader reaches.")
    print(f"\n{'='*64}\nrows that could not be normalized: {bad}")
    return 1 if bad else 0

def template():
    w = csv.writer(sys.stdout); w.writerow(list(FIELDS))
    w.writerow(["Mistral-7B","","","Q4_K_M","4.83","16","","","","","",
                "2048","512","RTX 4090","","100.43","1","mixed","yes","no","","","",""])
    print("# one example row above; delete it and add your own.", file=sys.stderr)
    for k,(eq,desc) in FIELDS.items():
        print(f"# {k:18s} [{eq:9s}] {desc}", file=sys.stderr)

def reproduce():
    import pandas as pd
    c = pd.read_csv("/home/claude/review/t2_normalized.csv")
    rows=[]
    for r in c.itertuples():
        lp = r.l_prompt if not pd.isna(r.l_prompt) else r.ctx
        lg = r.l_gen if not pd.isna(r.l_gen) else 0
        rows.append(dict(model=r.model, params_b="", active_b="", container=r.fmt,
            bits_per_weight=f"{r.bpw:.4f}", kv_bits=16, layers="", kv_heads="",
            head_dim="", sliding_window="", window_pattern="",
            prompt_tokens=int(lp), generated_tokens=int(lg), gpu=r.gpu,
            bandwidth_gbs="", tok_s=r.tok_s, batch=int(r.batch), phase=r.phase,
            resident="yes" if r.regime=="resident" else "no", speculative="no",
            spec_accept="", power_w="", energy_j_tok="", energy_window=""))
    out="/home/claude/review/table2_reproduction.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"wrote {out}\n"); return run(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
         formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from-csv", metavar="FILE")
    ap.add_argument("--template", action="store_true")
    ap.add_argument("--reproduce-table2", action="store_true")
    a = ap.parse_args()
    if a.template: template()
    elif a.reproduce_table2: sys.exit(reproduce())
    elif a.from_csv: sys.exit(run(a.from_csv))
    else: ap.print_help()
