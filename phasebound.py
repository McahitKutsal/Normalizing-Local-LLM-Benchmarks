"""
Sec. VII-A: bounding the mixed-phase contamination of the engine result.

The four measurements behind the 1.58x engine ratio report prefill and decode
together. The worry is that a compiled engine wins more on prefill -- which is
compute-bound, where kernel quality matters most -- and that the win is then
misattributed to decode bandwidth efficiency. The worry is reasonable and the
token counts appear to support it: at ISL 2048 / OSL 512, 80% of the tokens
processed are prefill tokens.

But a throughput figure divides by TIME, not by tokens, and prefill is roughly
sixty times faster per token than decode on this hardware class. Its share of
the wall clock is therefore small, and Amdahl's law caps what it can contribute.

Anchor: llama.cpp's own CUDA scoreboard reports, for Llama-2-7B Q4_0 on an
RTX 4090, pp512 = 11992.70 +- 107.99 t/s and tg128 = 186.21 +- 0.13 t/s.
"""
import numpy as np

PP, TG = 11992.70, 186.21        # llama.cpp CUDA scoreboard, RTX 4090, 7B Q4
LP, LG = 2048, 512               # Menlo ISL / OSL
RAW, NORM = 1.6614, 1.5840       # pooled raw and MBU ratios from corpus.py
BTOK_RATIO = 4.4520 / 4.6720     # AWQ-4 vs Q4_K_M per-token traffic

def prefill_time_share(lp, lg, pp, tg):
    """Fraction of wall-clock time spent in prefill."""
    return (lp / pp) / (lp / pp + lg / tg)

f = prefill_time_share(LP, LG, PP, TG)
print(f"prompt tokens are {100*LP/(LP+LG):.0f}% of all tokens processed")
print(f"prefill is {100*f:.2f}% of wall-clock time   (pp/tg speed ratio = {PP/TG:.1f}x)")
print(f"Amdahl cap -- maximum overall speedup from prefill alone: {1/(1-f):.3f}x\n")

thresh_raw  = 1 - 1/RAW
thresh_norm = 1 - 1/NORM
print(f"For prefill ALONE to explain the gap, its time share would have to be")
print(f"  >= {100*thresh_raw:.1f}% for the raw {RAW:.2f}x ratio")
print(f"  >= {100*thresh_norm:.1f}% for the normalized {NORM:.2f}x ratio")
print(f"  measured share is {100*f:.2f}%, i.e. {thresh_norm/f:.1f}x smaller. "
      f"Prefill cannot carry the result.\n")

def decode_ratio(total_ratio, f, s_prefill):
    """Decode-only speedup implied by an overall mixed-phase ratio."""
    rem = 1.0 / total_ratio - f / s_prefill
    return np.nan if rem <= 0 else (1.0 - f) / rem

print("Decode-only engine ratio under the two limiting scenarios:")
rows = []
for name, sp in [("engines equal at prefill (s_P = 1)", 1.0),
                 ("prefill win unbounded (s_P -> inf)", 1e9)]:
    dr_raw  = decode_ratio(RAW,  f, sp)
    dr_norm = dr_raw * BTOK_RATIO
    rows.append((name, dr_raw, dr_norm))
    print(f"  {name:36s} raw {dr_raw:.3f}x -> MBU {dr_norm:.3f}x")

lo = min(r[2] for r in rows); hi = max(r[2] for r in rows)
print(f"\n  decode-only MBU ratio lies in [{lo:.2f}, {hi:.2f}]")
print(f"  mixed-phase measured value is {NORM:.2f}x, inside that interval")
print(f"  worst-case displacement: {100*max(abs(hi-NORM), abs(lo-NORM))/NORM:.1f}%")

print("\nRobustness: the conclusion survives a wrong prefill-rate anchor.")
print("  prefill share f   ->  decode-only MBU ratio interval")
for ftest in [0.03, f, 0.10, 0.20, 0.30]:
    a = decode_ratio(RAW, ftest, 1.0) * BTOK_RATIO
    b = decode_ratio(RAW, ftest, 1e9) * BTOK_RATIO
    mark = "  <- measured" if abs(ftest - f) < 1e-9 else ""
    print(f"   {100*ftest:5.1f}%            [{min(a,b):.2f}, {max(a,b):.2f}]{mark}")
print(f"\n  Even at a prefill share five times the measured one, the decode-only")
print(f"  ratio stays above {decode_ratio(RAW,0.30,1e9)*BTOK_RATIO:.2f}x.")
