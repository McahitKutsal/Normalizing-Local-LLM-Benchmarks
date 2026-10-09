"""
Figure 2 and Sec. IV-F: how large a mislabelling must be before the filter notices.

Setup. Suppose a measurement was really taken at batch B with true per-stream
efficiency eta -- the fraction of the batch-B aggregate ceiling actually achieved
-- and is then presented as single-stream. At batch B the weights are read once
per sweep and shared across B streams, while each stream keeps its own cache, so
per-token traffic is B_w/B + B_kv and the aggregate ceiling is

    T_agg(B) = BW / (B_w/B + B_kv).

A reader who normalizes the reported T as batch-1 divides by B_tok = B_w + B_kv,
so with r = B_kv/B_w the cache share,

    MBU_computed = eta * (1 + r) / (1/B + r).                           (*)

The filter fires when that exceeds one, i.e. when

    eta > (1/B + r) / (1 + r).                                         (**)

Two consequences follow directly and neither is obvious from the qualitative
claim that the filter is "conservative":

  - With a negligible cache (r -> 0) the threshold is eta > 1/B. The filter sees
    a batch-2 measurement only if the run was better than 50% efficient, and a
    batch-4 one only above 25%. Ordinary efficiencies pass unnoticed.
  - As B grows the threshold tends to r/(1+r), NOT to zero. A workload whose
    cache dominates its traffic can be batched arbitrarily and still escape, so
    long-context measurements are the filter's blind spot.
"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figsave import save_figure
from normalize import MODELS, bits_per_weight, bytes_per_token, ctx_bar, gpu, BPW

G = gpu.set_index("gpu").to_dict("index")

def mbu_computed(eta, B, r):
    return eta * (1.0 + r) / (1.0 / B + r)

def eta_threshold(B, r):
    return (1.0 / B + r) / (1.0 + r)

# --- the corpus's own flagged rows, placed in this plane --------------------
CB = ctx_bar(8192, 512)
w, kv, bt = bytes_per_token("Qwen3-8B", "NVFP4", CB)
r_knoop = kv / w
KNOOP = [("5090", "RTX 5090", 411.0), ("5070 Ti", "RTX 5070 Ti", 211.0),
         ("5060 Ti", "RTX 5060 Ti 16GB", 115.0)]
print(f"Knoop rows: B_w {w/1e9:.3f} GB, B_kv {kv/1e9:.3f} GB, cache share r = {r_knoop:.3f}")
print(f"detection threshold at batch 8 with this r: eta > {eta_threshold(8, r_knoop):.3f}\n")
rows = []
for lbl, g, t in KNOOP:
    bw = G[g]["bw_gbs"] * 1e9
    m_obs = t * bt / bw
    eta_true = m_obs / ((1 + r_knoop) / (1 / 8 + r_knoop))
    rows.append((lbl, m_obs, eta_true, eta_threshold(8, r_knoop)))
    print(f"  {lbl:8s} MBU_computed {m_obs:.3f} -> implied true per-stream efficiency "
          f"{eta_true:.3f}  (threshold {eta_threshold(8,r_knoop):.3f}, "
          f"margin {100*(eta_true/eta_threshold(8,r_knoop)-1):+.0f}%)")

print(f"\ndetection thresholds at r = {r_knoop:.3f} (the corpus's flagged configuration):")
for B in [2, 4, 8, 16, 32]:
    print(f"  batch {B:2d}: eta > {eta_threshold(B, r_knoop):.3f}")
print(f"\nasymptote as batch -> infinity: eta > {r_knoop/(1+r_knoop):.3f} "
      f"(a cache-dominated run can never be caught)")

# low-cache comparison: the Menlo configuration
w2, kv2, _ = bytes_per_token("Mistral-7B", "AWQ-4", ctx_bar(2048, 512))
r_lo = kv2 / w2
print(f"\nfor comparison, the Menlo configuration has r = {r_lo:.3f}:")
for B in [2, 4, 8]:
    print(f"  batch {B:2d}: eta > {eta_threshold(B, r_lo):.3f}")

# --- the figure ------------------------------------------------------------
Bs  = np.logspace(0, 5, 500, base=2.0)      # 1 .. 32
eta = np.linspace(0.08, 1.0, 500)
BB, EE = np.meshgrid(Bs, eta)

fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6), sharey=True)
for ax, (frac, title) in zip(axes, [(1.00, "(a) against vendor peak bandwidth"),
                                    (0.85, "(b) against 85% achievable bandwidth")]):
    Z = mbu_computed(EE, BB, r_knoop) / frac
    # Two regions only: what the filter sees and what it does not. Printing in
    # grayscale must not lose the distinction, so the fill is light and the
    # information is carried by the labelled contours.
    ax.contourf(BB, EE, Z, levels=[0, 1, 1e6], colors=["#f2f2f2", "#f7d9c4"])
    cl = ax.contour(BB, EE, Z, levels=[0.5, 0.75, 1.5, 2, 3, 4],
                    colors="#8a8a8a", linewidths=.7)
    ax.clabel(cl, fmt="%.2g", fontsize=7, inline=True)
    ax.contour(BB, EE, Z, levels=[1.0], colors="k", linewidths=2.4)

    ax.set_xscale("log", base=2)
    ax.set_xticks([1, 2, 4, 8, 16, 32]); ax.set_xticklabels(["1","2","4","8","16","32"])
    ax.set_xlabel("True batch / concurrency $B$")
    ax.set_title(title, fontsize=10)
    ax.set_ylim(0.08, 1.0); ax.set_xlim(1, 32)

    # the corpus's three flagged rows
    for lbl, m_obs, eta_true, _ in rows:
        ax.plot(8, eta_true, "o", ms=6.5, mfc="white", mec="k", mew=1.4, zorder=6)
    # asymptotic floor: below this the filter can never fire, at any batch
    floor = r_knoop/(1+r_knoop) * frac
    ax.axhline(floor, color="k", ls=":", lw=1.0)
    ax.text(1.25, floor - .035, f"$\\eta={floor:.2f}$: unreachable at any batch",
            fontsize=7.4, ha="left", style="italic")

    ax.text(5.0, .115, "FILTER SILENT", fontsize=8.6, weight="bold", color="#555555")
    ax.text(26.5, .93, "DETECTED", fontsize=8.6, weight="bold", color="#9c4a1a", ha="right")

axes[0].set_ylabel("True per-stream efficiency  $\\eta$")
axes[0].annotate("the three flagged\ncorpus rows ($B=8$)", xy=(8.3, rows[0][2]),
                 xytext=(1.9, .74), fontsize=8.2,
                 arrowprops=dict(arrowstyle="->", lw=.9, color="k"))
axes[0].annotate("detection boundary\nMBU $=1$", xy=(13.5, eta_threshold(13.5, r_knoop)),
                 xytext=(9.0, .80), fontsize=8.2, ha="center",
                 arrowprops=dict(arrowstyle="->", lw=.9, color="k"))

fig.suptitle("A batch-$B$ measurement presented as single-stream is caught only "
             "above $\\eta \\approx 1/B$", fontsize=11.2, y=.98)
fig.tight_layout(rect=[0, 0, 1, .93])
save_figure(fig, "fig2_sensitivity")
print("\nwrote fig2_sensitivity.png")

pd.DataFrame(rows, columns=["gpu","mbu_computed","eta_implied","eta_threshold"]).to_csv(
    "/home/claude/review/t_sensitivity.csv", index=False)
