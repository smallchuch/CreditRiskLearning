"""
eda — exploratory plots and quick summaries for the PD model projects.

Design rules for anything added here:
  * Take data in as an argument (df / Series) — never read a global `df`.
    That keeps every function portable across projects and testable.
  * Return the figure/axes (or the computed object); let the caller decide
    when to `plt.show()` and what to tweak per group.
  * Keep sensible keyword defaults so the common call is one line.

Contents
--------
histogram_per_group : grid of histograms for numeric columns.
frequency_per_group : grid of frequency bars for categorical columns.
"""

import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .style import p, f, s, C, chart_title


def histogram_per_group(data, cols, *, ncols=3, bins=50, xlabel="Value",
                        color=None, kde=False, sharex=False, suptitle=None,
                        panel_w=9.0, panel_h=3.2, numeric_only=True, logx=False):
    """
    Draw a tidy grid of histograms, one panel per column.

    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to pull columns from (passed in, not global).
    cols : list[str]
        Columns to plot — e.g. cols_by_theme['external_scores'].
    ncols : int, default 3
        Panels per row; rows are derived from len(cols).
    bins : int, default 50
        Histogram bins. Fewer (20-30) for spiky data, more for smooth.
    xlabel : str, default "Value"
        Shared x-axis label (the measured value, not "bin").
    color : str, optional
        Bar colour; defaults to brand jacaranda.
    kde : bool, default False
        Overlay a KDE. Good for bounded/smooth features, skip for heavy skew.
    sharex : bool, default False
        Share the x-axis across panels — only when columns share a scale.
    suptitle : str, optional
        Optional figure-level title (e.g. the group name).
    panel_w, panel_h : float
        Width/height in inches per panel. Total figure size scales with the
        grid: (panel_w * ncols, panel_h * nrows). Bump these to enlarge.
    numeric_only : bool, default True
        Silently drop non-numeric columns (strings/categoricals) before
        plotting, since histograms need numeric data. Set False to force all.
    logx : bool, default False
        Bin and scale the x-axis in log space. Use for heavily right-skewed
        features (income, credit) so bins are even on a log axis. Requires
        positive values — non-positive rows are ignored by seaborn.

    Returns
    -------
    (fig, axes) : so the caller can apply per-group tweaks, e.g.
        fig, axes = histogram_per_group(df, cols, sharex=True)
        for ax in axes:
            ax.set_xlim(0, 1)
        plt.show()
    """
    color = color or p("jacaranda", 300)

    if numeric_only:   # histograms need numeric data — drop string/categorical cols
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(data[c])]

    n = len(cols)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(panel_w * ncols, panel_h * nrows),
                             sharex=sharex)
    axes = np.array(axes).reshape(-1)   # normalise 1x1 / 1-D / 2-D to a flat array

    for ax, col in zip(axes, cols):
        series = data[col].dropna()
        sns.histplot(series, bins=bins, ax=ax, color=color,
                     edgecolor="white", linewidth=0.5, alpha=0.85, kde=kde,
                     log_scale=logx)   # logx bins AND scales the x-axis in log space
        ax.axvline(series.median(), color=C.text_muted, ls="--", lw=1)   # median reference
        chart_title(ax, col.replace("_", " ").title(),
                    f"n={len(series):,} · {data[col].isna().mean():.0%} missing")
        ax.set_xlabel(xlabel)
        ax.grid(axis="y")
        ax.grid(axis="x", visible=False)

    for ax in axes[n:]:          # blank any leftover panels in the grid
        ax.set_visible(False)

    if suptitle:
        fig.suptitle(suptitle, fontfamily=f("heading"), fontsize=s("display"))

    fig.tight_layout(h_pad=2)
    return fig, axes


def frequency_per_group(data, cols, *, ncols=2, top_n=15, dropna=False,
                        pct=False, color=None, suptitle=None,
                        panel_w=7.0, panel_h=4.0, categorical_only=True):
    """
    Draw a grid of frequency bar charts, one panel per categorical column.

    The string/categorical counterpart to `histogram_per_group`: horizontal
    bars sorted by frequency, with the long tail pooled into an "Other" bar and
    missing values shown as their own bar so nothing is hidden.

    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to pull columns from (passed in, not global).
    cols : list[str]
        Categorical columns to plot — e.g. cols_by_type['categorical'].
    ncols : int, default 2
        Panels per row; rows derived from len(cols).
    top_n : int or None, default 15
        Show only the top-N levels by frequency; the remainder are pooled into
        a single "Other (k more)" bar so the total is preserved. None = show all.
    dropna : bool, default False
        If False, missing values appear as their own "Missing" bar.
    pct : bool, default False
        Plot share of rows instead of raw counts.
    color : str, optional
        Bar colour; defaults to brand jacaranda.
    suptitle : str, optional
        Optional figure-level title (e.g. the group name).
    panel_w, panel_h : float
        Width/height in inches per panel. Figure scales to
        (panel_w * ncols, panel_h * nrows).
    categorical_only : bool, default True
        Silently drop numeric columns, so you can pass a mixed theme group
        (e.g. cols_by_theme['loan_financials']) and only its string/categorical
        columns are charted. Mirror of numeric_only in histogram_per_group.
        Set False to force numeric columns through as discrete categories.

    Returns
    -------
    (fig, axes) : for per-panel tweaks after the call, same as histogram_per_group.
    """
    color = color or p("jacaranda", 300)

    if categorical_only:   # bar charts are for categoricals — drop numeric cols
        cols = [c for c in cols if not pd.api.types.is_numeric_dtype(data[c])]

    n = len(cols)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(panel_w * ncols, panel_h * nrows))
    axes = np.array(axes).reshape(-1)

    for ax, col in zip(axes, cols):
        counts = data[col].value_counts(dropna=dropna)
        total = counts.sum()

        # pool the long tail beyond top_n into a single "Other" bar
        if top_n is not None and len(counts) > top_n:
            other = counts.iloc[top_n:].sum()
            counts = counts.iloc[:top_n]
            counts[f"Other ({data[col].nunique() - top_n} more)"] = other

        if pct:
            counts = counts / total

        counts = counts.sort_values()   # ascending → largest bar on top in barh
        labels = ["Missing" if pd.isna(i) else str(i) for i in counts.index]

        bars = ax.barh(labels, counts.values, color=color, alpha=0.85,
                       edgecolor="white", linewidth=0.5)
        fmt = "{:.1%}".format if pct else "{:,.0f}".format
        ax.bar_label(bars, labels=[fmt(v) for v in counts.values],
                     padding=3, fontsize=s("small"), fontfamily=f("mono"))

        chart_title(ax, col.replace("_", " ").title(),
                    f"{data[col].nunique():,} levels · {data[col].isna().mean():.0%} missing")
        ax.set_xlabel("Share" if pct else "Count")
        ax.grid(axis="x")
        ax.grid(axis="y", visible=False)
        ax.margins(x=0.12)   # headroom for the value labels

    for ax in axes[n:]:      # blank any leftover panels
        ax.set_visible(False)

    if suptitle:
        fig.suptitle(suptitle, fontfamily=f("heading"), fontsize=s("display"))

    fig.tight_layout(h_pad=2)
    return fig, axes
