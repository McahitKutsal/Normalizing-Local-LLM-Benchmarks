"""
Shared figure writer: guarantees an effective resolution at the width each figure
is actually placed, and emits a vector copy alongside.

Effective dpi is not the dpi passed to savefig. matplotlib multiplies figsize by
dpi to get pixels, then `bbox_inches="tight"` trims the margins away, and the
manuscript then stretches or squeezes the result to a fixed width in inches. What
matters for print is pixels divided by THAT width, so this writer measures the
saved file and re-saves at a higher dpi if the trimmed image falls short.

PLACED_IN mirrors the widths in paper/build.js. If a figure's placement changes
there, change it here too; check_dpi() in audit.py compares the two and fails if
they drift apart.
"""
import pathlib
from PIL import Image

R = pathlib.Path("/home/claude/review")
TARGET_DPI = 600          # IEEE Access asks 600 for line art; 300 is the floor
PLACED_IN = {             # figure stem -> width in inches as build.js places it
    "fig1_framework":   6.5,
    "fig2_sensitivity": 7.0,
    "fig3_quality":     6.7,
    "fig4_context":     6.2,
    "fig5_energy_cost": 6.7,
    "fig6_roofline":    6.3,
}

def save_figure(fig, stem, vector=True, _dpi=TARGET_DPI, _tries=3):
    """Write <stem>.png at >= TARGET_DPI effective, plus <stem>.pdf as vector."""
    if stem not in PLACED_IN:
        raise KeyError(f"{stem!r} has no placement width; add it to PLACED_IN")
    placed = PLACED_IN[stem]
    png = R / f"{stem}.png"
    for attempt in range(_tries):
        fig.savefig(png, dpi=_dpi)
        px = Image.open(png).size[0]
        eff = px / placed
        if eff >= TARGET_DPI:
            break
        # trimming removed more than expected; scale the request by the shortfall
        _dpi = int(_dpi * (TARGET_DPI / eff) * 1.02) + 1
    else:
        raise RuntimeError(f"{stem}: could not reach {TARGET_DPI} dpi effective")
    if vector:
        fig.savefig(R / f"{stem}.pdf")        # resolution-independent for camera-ready
    print(f"  {stem:20s} {px:5d}px / {placed}in = {eff:4.0f} dpi effective "
          f"(saved at {_dpi})")
    return eff

def report():
    """Effective dpi of every figure currently on disk."""
    out = {}
    for stem, placed in PLACED_IN.items():
        p = R / f"{stem}.png"
        if p.exists():
            out[stem] = Image.open(p).size[0] / placed
    return out
