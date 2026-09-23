"""
deck_utils — shared helpers for the Flagship PD Model reveal.js decks.

Import this in a stage deck's setup cell so every stage (EDA / PD / LGD / EAD)
shares one chart-styling system and the same figure helpers. Pairs with
`brand.scss` (the slide theme). Single source of truth lives here + in
python_style_util.py, so restyling one file restyles every deck.

    from deck_utils import deck_style, BRAND_RAMP, add_baseline, strip_bar_labels
    deck_style()
    fig, axes = default_rate_by_bin(df, cols, "TARGET", grade_scale=BRAND_RAMP,
                                    show_base_rate=False, panel_w=5.0, panel_h=4.7)
    add_baseline(axes, BASE)
"""

import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import python_style_util as psu
from python_style_util import set_style, C, f

# Clean purple sequential ramp for graded bars: light lilac (low default rate)
# -> deep jacaranda (high). No muddy purple->gold mid-tones; gold is reserved
# for slide furniture. Swap these four hexes to reskin every chart's bars.
BRAND_RAMP = mcolors.LinearSegmentedColormap.from_list(
    "brand_purple", ["#CDBFE0", "#8E74AE", "#5C4577", "#3D2E4F"])


def deck_style():
    """Apply brand matplotlib defaults tuned for slide-scale legibility.
    Call once at the top of a deck's setup cell (after imports)."""
    psu.sizes.update({"title": 15, "subtitle": 13, "body": 12,
                      "small": 12, "tiny": 11, "mono": 12})
    set_style()
    plt.rcParams.update({
        "figure.dpi": 130, "savefig.dpi": 130,
        "axes.titlesize": 15, "axes.titlepad": 8,
        "xtick.labelsize": 12, "ytick.labelsize": 12, "axes.labelsize": 12,
    })


def small_labels(n=9):
    """Shrink per-bar value labels for a dense chart (call before plotting)."""
    psu.sizes["small"] = n


def reset_labels():
    """Restore the default per-bar label size."""
    psu.sizes["small"] = 12


def add_baseline(axes, base):
    """Draw the base-rate reference line with its label parked on a white chip
    in the right margin, lifted clear of the line so it never touches a bar
    label. Use with default_rate_by_bin(..., show_base_rate=False)."""
    for ax in np.ravel(np.asarray(axes)):
        ax.axhline(base, ls="--", color=C.text_muted, lw=1, zorder=1.4)
        ax.annotate(f"base {base:.1%}", xy=(0.992, base),
                    xycoords=ax.get_yaxis_transform(),
                    xytext=(0, 4), textcoords="offset points",
                    ha="right", va="bottom", fontsize=10, color=C.text_muted,
                    fontfamily=f("mono"), zorder=5,
                    bbox=dict(facecolor="white", edgecolor="none",
                              boxstyle="round,pad=0.2", alpha=0.9))


def strip_bar_labels(axes):
    """Remove per-bar percentage labels (keeps titles/subtitles). For dense
    panels (e.g. 12 near-equal bins) where labels would collide — the y-axis
    carries the values and the panel's point is the shape, not the digits."""
    for ax in np.ravel(np.asarray(axes)):
        for t in list(ax.texts):
            if re.fullmatch(r"\d+(\.\d+)?%", t.get_text().strip()):
                t.remove()
