import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

C1, INK, INK2, MUTED, GRID, SURF = "#2a78d6", "#0b0b0b", "#52514e", "#8a8985", "#e3e2de", "#fcfcfb"
EXC = "#f7f7f6"

plt.rcParams.update({"figure.facecolor": SURF, "font.family": "DejaVu Sans",
                     "savefig.dpi": 300, "savefig.bbox": "tight"})
fig, ax = plt.subplots(figsize=(7.0, 6.0))
ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, lines, fill=SURF, edge=C1, lw=1.3, fs=7.6, bold_first=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6,rounding_size=1.2",
                                facecolor=fill, edgecolor=edge, linewidth=lw, zorder=2))
    n = len(lines)
    for i, t in enumerate(lines):
        ax.text(x + w/2, y + h - (h/(n+1))*(i+1), t, ha="center", va="center",
                fontsize=fs, color=INK if i == 0 else INK2,
                fontweight="bold" if (i == 0 and bold_first) else "normal", zorder=3)

def arrow(x1, y1, x2, y2, color=MUTED):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                                 color=color, linewidth=1.1, zorder=1,
                                 shrinkA=0, shrinkB=0))

# stage labels down the left margin
for y, lab in [(90, "Identification"), (62, "Screening"), (34, "Eligibility"), (12, "Included")]:
    ax.text(2.0, y, lab, rotation=90, ha="center", va="center", fontsize=7.6,
            color=C1, fontweight="bold")

# main column
box(12, 83, 48, 14, ["Records identified via databases",
                     "arXiv, IEEE Xplore, ACM DL,",
                     "ScienceDirect, Semantic Scholar",
                     "n = 1,486"], fs=7.2)
box(12, 66, 48, 11, ["Records after duplicate removal", "n = 1,092"])
box(12, 48, 48, 11, ["Records screened on title and abstract", "n = 1,092"], fs=7.2)
box(12, 28, 48, 13, ["Full-text reports assessed", "for eligibility", "n = 138"], fs=7.4)
box(12, 5,  48, 15, ["Studies included in the review", "n = 47",
                     "Measurements extracted and normalized", "n = 19"],
    edge=C1, lw=1.9, fs=7.2)

# supplementary source
box(67, 83, 31, 14, ["Records from other sources",
                     "vendor and inference-engine", "engineering reports", "n = 41"],
    edge=MUTED, lw=1.0, fs=6.8)
arrow(82.5, 83, 82.5, 73); arrow(82.5, 73, 60.5, 71.5)

# exclusion boxes
box(67, 45, 31, 14, ["Records excluded", "n = 954",
                     "off-topic, datacenter-only,", "no measurement reported"],
    fill=EXC, edge=MUTED, lw=1.0, fs=6.8)
box(67, 23, 31, 16, ["Full texts excluded", "n = 91",
                     "42 not normalizable", "27 no consumer GPU",
                     "14 training only, 8 no data"], fill=EXC, edge=MUTED, lw=1.0, fs=6.8)

# flow arrows
arrow(36, 83, 36, 77)
arrow(36, 66, 36, 59)
arrow(36, 48, 36, 41)
arrow(36, 28, 36, 20)
arrow(60.5, 53.5, 67, 52)
arrow(60.5, 34.5, 67, 31)

ax.text(48, 101, "Identification of studies via databases and supplementary sources",
        ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
fig.savefig("/home/claude/review/fig1_prisma.png")
print("fig1 written")
