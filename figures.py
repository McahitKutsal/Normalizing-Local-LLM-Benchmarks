import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from figsave import save_figure
from matplotlib.ticker import FuncFormatter
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd, numpy as np

C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8985", "#e3e2de", "#fcfcfb"

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF,
    "font.family": "DejaVu Sans", "font.size": 9,
    "axes.edgecolor": GRID, "axes.linewidth": 0.8,
    "axes.labelcolor": INK2, "text.color": INK,
    "xtick.color": INK2, "ytick.color": INK2,
    "xtick.labelsize": 8, "ytick.labelsize": 8,
    "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.alpha": 0.9,
    "legend.frameon": False, "legend.fontsize": 8,
    "savefig.dpi": 600, "savefig.bbox": "tight",
})
def despine(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)
    ax.set_axisbelow(True)

df = pd.read_csv("/home/claude/review/t2_normalized.csv")
q  = pd.read_csv("/home/claude/review/t4_quality.csv")
fr = pd.read_csv("/home/claude/review/t3_frontier.csv")
en = pd.read_csv("/home/claude/review/t5_energy.csv")
cd = pd.read_csv("/home/claude/review/t6_cost.csv")

# ============ FIG 1: the normalization pipeline ============
fig, ax = plt.subplots(figsize=(7.0, 3.5))
ax.set_xlim(-2.5, 102.5); ax.set_ylim(-1, 54); ax.axis("off")

def box(x, y, w, h, title, lines, edge=C1, fill=SURF, lw=1.3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.0",
                                facecolor=fill, edgecolor=edge, linewidth=lw, zorder=2))
    ax.text(x+w/2, y+h-3.2, title, ha="center", va="center", fontsize=8,
            fontweight="bold", color=INK, zorder=3)
    for i, t in enumerate(lines):
        ax.text(x+w/2, y+h-8.0-i*4.4, t, ha="center", va="center",
                fontsize=6.9, color=INK2, zorder=3)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=11, color=MUTED, linewidth=1.1,
                                 zorder=1, shrinkA=0, shrinkB=0))

box(0, 20, 21, 25, "Reported figure",
    ["tokens / second", "engine, device,", "container, context"], edge=MUTED, lw=1.0)
box(26, 20, 21, 25, "Per-token traffic",
    ["$B_w$ from eff. bits/wt", "$B_{kv}$ window-aware", "Eq. (1)-(4)"])
box(52, 20, 21, 25, "Device ceiling",
    ["$T_{max} = BW / B_{tok}$", "VRAM or PCIe bound", "Eq. (5)"])
box(78, 20, 21, 25, "Normalized",
    ["MBU, tok/s per TB/s", "J/token, USD/MTok", "Eq. (6)-(9)"], edge=C3)
for x in (21, 47, 73):
    arrow(x, 32.5, x+5, 32.5)

box(19, 1, 62, 14, "Validity filter",
    ["MBU > 1 cannot describe batch-1 decode: flag the row,",
     "report the implied batch size (Sec. IV-E)"],
    edge=C2, fill="#fdf3ef", lw=1.2)
arrow(62.5, 20, 62.5, 15)

ax.text(50, 53, "Any reported measurement, reduced to a device-independent basis",
        ha="center", va="top", fontsize=9, fontweight="bold", color=INK)
save_figure(fig, "fig1_framework"); plt.close(fig)

# ============ FIG 2: accuracy vs compression (verified) ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
qs = q[q.quant != "F16"].sort_values("bpw", ascending=False)
def grp(b):
    return C1 if b >= 5.5 else (C2 if b >= 4.0 else C3)
cols = [grp(b) for b in qs.bpw]

ax = axes[0]
ax.axhline(0, color=GRID, lw=1.0, zorder=1)
ax.plot(qs.bpw, qs.d_avg_pp, color=MUTED, lw=1.4, zorder=2)
ax.scatter(qs.bpw, qs.d_gsm8k_pp, s=28, c=cols, marker="^", lw=0.8,
           edgecolors=SURF, zorder=3, alpha=0.75, label="GSM8K alone")
ax.scatter(qs.bpw, qs.d_avg_pp, s=46, c=cols, lw=1.1, edgecolors=SURF, zorder=4,
           label="5-task mean")
ax.set_xlim(9.2, 3.2); ax.set_ylim(-2.4, 10.2)
ax.set_xlabel("Effective bits per weight")
ax.set_ylabel("Accuracy lost vs FP16 (pp)")
ax.set_title("(a) Accuracy cost", loc="left")
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], loc="upper left", fontsize=7,
          handletextpad=0.4, labelspacing=0.35)
# Label the five-task-mean marker only, with a short leader where the label
# cannot sit next to its point without touching a neighbour.
for lbl, x, y, dx, dy, ha in [("Q5_K_M", 5.704, 0.11, -6, 30, "right"),
                              ("Q4_K_M", 4.894, 0.32, 2, -22, "center"),
                              ("Q4_0",   4.635, 1.49, 14, 6, "left"),
                              ("Q3_K_M", 3.995, 1.40, 14, -8, "left"),
                              ("Q3_K_S", 3.643, 3.98, 13, -2, "left")]:
    ax.annotate(lbl, (x, y), xytext=(dx, dy), textcoords="offset points",
                fontsize=7, color=INK2, ha=ha,
                arrowprops=dict(arrowstyle="-", color=GRID, lw=0.7,
                                shrinkA=1, shrinkB=3))
ax.annotate("GSM8K falls 9.3 pp", (3.643, 9.32), xytext=(10, 0),
            textcoords="offset points", fontsize=7, color="#12805a", va="center")
ax.axvspan(3.2, 4.0, color=C3, alpha=0.09, lw=0, zorder=0)
ax.text(3.6, -1.9, "sub-4-bit", fontsize=7, color="#12805a",
        ha="center", style="italic")
despine(ax)

ax = axes[1]
ax.plot(qs.bpw, qs.speedup, color=MUTED, lw=1.3, zorder=2)
ax.scatter(qs.bpw, qs.speedup, s=44, c=cols, lw=1.1, edgecolors=SURF, zorder=3)
ax.set_xlim(9.2, 3.2)
ax.set_xlabel("Effective bits per weight")
ax.set_ylabel("Roofline speedup vs FP16 ($\\times$)")
ax.set_title("(b) Throughput benefit", loc="left")
ax.axvspan(3.2, 4.0, color=C3, alpha=0.09, lw=0, zorder=0)
despine(ax)
fig.suptitle("Accuracy is near-free down to about 4.6 bits, then falls sharply below 4",
             fontsize=9.5, fontweight="bold", y=1.03)
fig.tight_layout()
save_figure(fig, "fig3_quality"); plt.close(fig)

# ============ FIG 3: context wall ============
fig, ax = plt.subplots(figsize=(6.4, 3.4))
order = ["Qwen3-8B", "Llama-3.1-8B", "Qwen2.5-32B", "Llama-3.3-70B",
         "Gemma-3-12B", "Gemma-3-27B"]
sub = fr[fr.fmt == "Q4_K_M"]
ctxs = sorted(sub.ctx.unique())
x = np.arange(len(order)); w = 0.26
for i, c in enumerate(ctxs):
    s = sub[sub.ctx == c].set_index("model").reindex(order)
    shade = [0.38, 0.68, 1.0][i]
    cols = [(C3 if MOD == "sliding" else C1) for MOD in s.window]
    cols = [matplotlib.colors.to_rgba(cc, shade) for cc in cols]
    ax.bar(x + (i-1)*w, s.kv_share, width=w*0.9, color=cols, zorder=3,
           edgecolor=SURF, linewidth=0.6,
           label=f"{c//1024}k context")
ax.set_xticks(x)
ax.set_xticklabels([m.replace("Llama-", "Llama ").replace("Gemma-", "Gemma ")
                    .replace("Qwen", "Qwen ") for m in order], fontsize=7.4)
ax.set_ylabel("KV cache share of footprint (%)")
ax.set_title("Full attention pays the context wall; interleaved windows do not")
ax.axvline(3.5, color=MUTED, lw=1.0, ls="--", zorder=2)
ax.text(1.5, 83, "full attention", ha="center", fontsize=8, color=C1, fontweight="bold")
ax.text(4.5, 83, "sliding window", ha="center", fontsize=8, color=C3, fontweight="bold")
ax.set_ylim(0, 92)
ax.grid(axis="x", visible=False)
h = [plt.Rectangle((0,0),1,1, color=matplotlib.colors.to_rgba(MUTED, s))
     for s in [0.38, 0.68, 1.0]]
ax.legend(h, [f"{c//1024}k context" for c in ctxs], loc="upper left", fontsize=7.5)
despine(ax)
save_figure(fig, "fig4_context"); plt.close(fig)

# ============ FIG 4: energy and cost ============
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))
e = en.sort_values("tok_s")
ax = axes[0]
ax.scatter(e.tok_s, e.J_per_tok, s=52, c=C1, lw=1.1, edgecolors=SURF, zorder=3)
z = np.polyfit(e.tok_s, e.J_per_tok, 1)
xs = np.linspace(e.tok_s.min()*0.92, e.tok_s.max()*1.05, 50)
ax.plot(xs, np.polyval(z, xs), color=MUTED, lw=1.2, ls="--", zorder=2)
for _, r in e.iterrows():
    if r.model in ("mistral:7b", "gemma3:1b", "phi4-mini:3.8b"):
        ax.annotate(r.model, (r.tok_s, r.J_per_tok), xytext=(7, 4),
                    textcoords="offset points", fontsize=7, color=INK2)
ax.set_xlabel("Decode throughput (tokens s$^{-1}$)")
ax.set_ylabel("Energy per token (J)")
ax.set_title("(a) Measured energy, RTX 4060 Ti", loc="left")
ax.text(0.97, 0.93, f"r = {np.corrcoef(e.tok_s, e.J_per_tok)[0,1]:.2f}",
        transform=ax.transAxes, ha="right", fontsize=8, color=INK2)
despine(ax)

ax = axes[1]
c = cd.sort_values("USD_total")
y = np.arange(len(c))
ax.barh(y, c.USD_elec, height=0.62, color=C1, label="Electricity", zorder=3)
ax.barh(y, c.USD_amort, left=c.USD_elec+0.002, height=0.62, color=C2,
        label="Hardware amortization", zorder=3)
ax.set_yticks(y); ax.set_yticklabels(c.model, fontsize=7)
ax.set_xlabel("USD per million generated tokens")
ax.set_title("(b) True cost decomposition", loc="left")
ax.legend(loc="lower right", fontsize=7)
ax.grid(axis="y", visible=False)
despine(ax)
_share = 100 * cd.USD_elec.sum() / cd.USD_total.sum()
fig.suptitle(f"Electricity is {_share:.0f}% of the true cost of a local token",
             fontsize=9.5, fontweight="bold", y=1.03)
fig.tight_layout()
save_figure(fig, "fig5_energy_cost"); plt.close(fig)

# ============ FIG 5: verified corpus against the roofline ============
fig, ax = plt.subplots(figsize=(6.6, 4.6))
# Axis range follows the surviving data. It used to reach down to 0.6 to hold an
# offloaded point at 16 tok/s against a 1.06 tok/s interconnect bound; that row was
# withdrawn (Sec. VII-C), so two thirds of the panel would otherwise be empty.
lim = [40, 700]
ax.plot(lim, lim, color=MUTED, lw=1.2, ls="--", zorder=1)
ax.fill_between(lim, lim, [lim[1]]*2, color="#e34948", alpha=0.055, zorder=0, lw=0)
ax.text(43, 430, "above the batch-1 ceiling:\nnot single-stream decode",
        color="#b03a39", fontsize=7.5, ha="left", va="center", style="italic")
for frac, lab, xa in [(0.5, "50% of ceiling", 230.0), (0.25, "25%", 430.0)]:
    ax.plot(lim, [l*frac for l in lim], color=GRID, lw=0.9, zorder=1)
    ax.text(xa, xa*frac*0.78, lab, fontsize=7, color=MUTED, ha="left",
            va="top", rotation=31, rotation_mode="anchor")

groups = [
    (df[(df.regime=="resident") & (~df.exceeds_b1)], C1, "o", "Single-stream, VRAM-resident"),
    (df[df.exceeds_b1],                              C2, "D", "Flagged: source confirms batching"),
]
for sub, col, mk, lab in groups:
    ax.scatter(sub.roofline_vram, sub.tok_s, s=66, c=col, marker=mk, lw=1.1,
               edgecolors=SURF, zorder=4, label=lab)

# The offloaded point that used to sit here was withdrawn: its throughput is
# published only inside a figure image, so it fails the inclusion rule of
# Sec. V-A. See Sec. VII-C.

for _, r in df[df.exceeds_b1].iterrows():
    ax.annotate(f"c=8", (r.roofline_vram, r.tok_s), xytext=(7, 3),
                textcoords="offset points", fontsize=7, color="#b03a39")

ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlim(lim); ax.set_ylim([40, 700])
from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
for axis in (ax.xaxis, ax.yaxis):
    axis.set_major_locator(FixedLocator([50, 100, 200, 400]))
    axis.set_major_formatter(ScalarFormatter())
    axis.set_minor_formatter(NullFormatter())
ax.set_xlabel("Bandwidth-bound ceiling at batch 1 (tokens s$^{-1}$)")
ax.set_ylabel("Reported throughput (tokens s$^{-1}$)")
ax.set_title("Every verified measurement against its computed ceiling")
for a in (ax.xaxis, ax.yaxis):
    a.set_major_formatter(FuncFormatter(lambda v, p: f"{v:g}"))
    a.set_minor_formatter(FuncFormatter(lambda v, p: ""))
ax.legend(loc="lower right", fontsize=7.5)
despine(ax)
save_figure(fig, "fig6_roofline"); plt.close(fig)

print("figures written")
