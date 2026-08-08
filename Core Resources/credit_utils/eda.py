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
overlaid_histogram_per_group : grid of histograms split/overlaid by a class variable.
default_rate_by_bin : grid of default-rate-per-bin bars for numeric columns.
frequency_per_group : grid of frequency bars for categorical columns.
"""

import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from .style import p, f, s, C, chart_title, binary_palette, multi_series


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


def overlaid_histogram_per_group(data, cols, by, *, ncols=3, bins=50,
                                 xlabel="Value", stat="density",
                                 common_norm=False, kde=False, sharex=False,
                                 suptitle=None, panel_w=9.0, panel_h=3.2,
                                 numeric_only=True, logx=False, palette=None,
                                 **kwargs):
    """
    Draw a grid of overlaid histograms, one panel per column, with each panel
    split into overlapping distributions by the `by` class variable.

    The two-group counterpart to `histogram_per_group`: instead of one bar
    stack per panel, each level of `by` (e.g. TARGET 0/1, OWNS_CAR Y/N) gets its
    own translucent histogram drawn on the same axes, so you can compare the
    shape of a feature across classes — e.g. EXT_SOURCE_1 for defaulters vs
    non-defaulters.

    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to pull columns from (passed in, not global).
    cols : list[str]
        Columns to plot — e.g. cols_by_theme['external_scores'].
    by : str
        Column whose levels split each distribution (the hue), e.g. 'TARGET'.
    ncols : int, default 3
        Panels per row; rows are derived from len(cols).
    bins : int, default 50
        Histogram bins, shared across the overlaid groups in each panel.
    xlabel : str, default "Value"
        Shared x-axis label (the measured value, not "bin").
    stat : str, default "density"
        seaborn histplot stat. "density" (default) makes imbalanced classes
        comparable — with raw "count" a rare class (e.g. defaulters) is dwarfed.
    common_norm : bool, default False
        When stat is a normalising stat, normalise each group independently
        (False) rather than across all groups, so each curve integrates to 1.
    kde : bool, default False
        Overlay a KDE per group.
    sharex : bool, default False
        Share the x-axis across panels — only when columns share a scale.
    suptitle : str, optional
        Optional figure-level title (e.g. the group name).
    panel_w, panel_h : float
        Width/height in inches per panel; figure scales to
        (panel_w * ncols, panel_h * nrows).
    numeric_only : bool, default True
        Silently drop non-numeric columns before plotting.
    logx : bool, default False
        Bin and scale the x-axis in log space (right-skewed features).
    palette : dict or list, optional
        Colour mapping for the `by` levels. Defaults to the brand
        binary_palette (non-default→green, default→red) for two classes,
        or multi_series() colours for more.
    **kwargs
        Extra keyword args forwarded straight to seaborn.histplot, overriding
        the styling defaults (element="step", edgecolor="white", linewidth=0.5,
        alpha=0.45). E.g. edgecolor="black", alpha=0.6, element="bars".

    Returns
    -------
    (fig, axes) : so the caller can apply per-group tweaks, same contract as
        histogram_per_group.
    """
    if numeric_only:   # histograms need numeric data — drop string/categorical cols
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(data[c])]

    hue_order = list(pd.Series(data[by].dropna().unique()).sort_values())
    if palette is None:
        palette = (binary_palette(labels=tuple(hue_order))
                   if len(hue_order) == 2
                   else dict(zip(hue_order, multi_series())))

    n = len(cols)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(panel_w * ncols, panel_h * nrows),
                             sharex=sharex)
    axes = np.array(axes).reshape(-1)   # normalise 1x1 / 1-D / 2-D to a flat array

    for ax, col in zip(axes, cols):
        sub = data[[col, by]].dropna(subset=[col])

        plot_kw = dict(element="step", edgecolor="white", linewidth=0.5,
                       alpha=0.45)   # defaults; caller kwargs override these
        plot_kw.update(kwargs)

        sns.histplot(data=sub, x=col, hue=by, hue_order=hue_order,
                     bins=bins, ax=ax, palette=palette, stat=stat,
                     common_norm=common_norm, common_bins=True,
                     kde=kde, log_scale=logx, **plot_kw)
        chart_title(ax, col.replace("_", " ").title(),
                    f"split by {by} · {data[col].isna().mean():.0%} missing")
        ax.set_xlabel(xlabel)
        ax.grid(axis="y")
        ax.grid(axis="x", visible=False)

    for ax in axes[n:]:          # blank any leftover panels in the grid
        ax.set_visible(False)

    if suptitle:
        fig.suptitle(suptitle, fontfamily=f("heading"), fontsize=s("display"))

    fig.tight_layout(h_pad=2)
    return fig, axes


def default_rate_by_bin(data, cols, target, *, ncols=3, bins=10,
                        method="quantile", xlabel="Bin (low → high)",
                        color=None, show_base_rate=True, suptitle=None,
                        panel_w=9.0, panel_h=3.2, numeric_only=True,
                        rotation=45, **kwargs):
    """
    Draw a grid of default-rate-per-bin bar charts, one panel per column.

    The workhorse bivariate plot for a binary target: bin each numeric feature,
    then show the mean of `target` (the default rate) within each bin. This
    exposes the *shape* of the risk relationship — monotonic, linear, threshold
    — which is what you check before scorecard binning / WOE encoding. Because
    binning a continuous feature turns it into "default rate per group", this is
    also the continuous counterpart to a categorical default-rate chart.

    Parameters
    ----------
    data : pd.DataFrame
        The dataframe to pull columns from (passed in, not global).
    cols : list[str]
        Columns to plot — e.g. cols_by_theme['external_scores'].
    target : str
        Binary (0/1) target column; its mean per bin is the default rate.
    ncols : int, default 3
        Panels per row; rows derived from len(cols).
    bins : int, default 10
        Number of bins (deciles by default).
    method : {"quantile", "width"}, default "quantile"
        "quantile" → equal-population bins via pd.qcut (recommended: stable
        default rates per bar). "width" → equal-width bins via pd.cut.
    xlabel : str, default "Bin (low → high)"
        Shared x-axis label.
    color : str, optional
        Bar colour; defaults to brand jacaranda.
    show_base_rate : bool, default True
        Draw a dashed line at the overall default rate for reference, so you can
        see which bins sit above/below average risk.
    suptitle : str, optional
        Optional figure-level title.
    panel_w, panel_h : float
        Width/height in inches per panel; figure scales to
        (panel_w * ncols, panel_h * nrows).
    numeric_only : bool, default True
        Silently drop non-numeric columns (binning needs numeric data).
    rotation : int, default 45
        Rotation for the bin-edge tick labels.
    **kwargs
        Extra keyword args forwarded to ax.bar (e.g. alpha, linewidth).

    Returns
    -------
    (fig, axes) : same contract as the other grid plotters.
    """
    color = color or p("jacaranda", 300)

    if numeric_only:   # binning needs numeric data — drop string/categorical cols
        cols = [c for c in cols if pd.api.types.is_numeric_dtype(data[c])]

    n = len(cols)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows, ncols,
                             figsize=(panel_w * ncols, panel_h * nrows))
    axes = np.array(axes).reshape(-1)

    base_rate = data[target].mean()

    for ax, col in zip(axes, cols):
        sub = data[[col, target]].dropna(subset=[col])

        cutter = pd.qcut if method == "quantile" else pd.cut
        sub = sub.assign(_bin=cutter(sub[col], bins, duplicates="drop"))

        grp = sub.groupby("_bin", observed=True)[target]
        rate = grp.mean()
        counts = grp.size()

        labels = [f"{iv.left:.2g}–{iv.right:.2g}" for iv in rate.index]
        bar_kw = dict(alpha=0.85, edgecolor="white", linewidth=0.5)
        bar_kw.update(kwargs)
        bars = ax.bar(range(len(rate)), rate.values, color=color, **bar_kw)

        ax.bar_label(bars, labels=[f"{v:.1%}" for v in rate.values],
                     padding=3, fontsize=s("small"), fontfamily=f("mono"))

        if show_base_rate:   # overall default rate reference
            ax.axhline(base_rate, color=C.text_muted, ls="--", lw=1)
            ax.text(len(rate) - 0.5, base_rate, f" base {base_rate:.1%}",
                    va="bottom", ha="right", fontsize=s("small"),
                    color=C.text_muted, fontfamily=f("mono"))

        ax.set_xticks(range(len(rate)))
        ax.set_xticklabels(labels, rotation=rotation, ha="right",
                           fontsize=s("small"))
        chart_title(ax, col.replace("_", " ").title(),
                    f"{method} bins · n={counts.sum():,} · "
                    f"{data[col].isna().mean():.0%} missing")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Default rate")
        ax.grid(axis="y")
        ax.grid(axis="x", visible=False)
        ax.margins(y=0.15)   # headroom for value labels

    for ax in axes[n:]:      # blank any leftover panels
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
