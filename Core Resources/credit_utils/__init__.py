"""
credit_utils — shared toolkit for the Credit Risk PD model projects.

Grow this deliberately: add a function only once you've written it twice in a
notebook and know it works. That way you always know what's in here and how to
use it.

Modules
-------
style    : brand colours, fonts, chart styling   (re-exports python_style_util)
eda      : exploratory plots & summaries          -> histogram_per_group
quality  : data-quality & cleaning helpers        (empty — add as we go)
woe      : Weight-of-Evidence / Information Value  (empty — add in Section 5)
stats    : hypothesis tests for driver checks      (empty — add in Section 4)

Typical use in a notebook
--------------------------
    %load_ext autoreload
    %autoreload 2

    from credit_utils.style import set_style, p, f, s
    from credit_utils.eda import histogram_per_group

    set_style()
    fig, axes = histogram_per_group(df, cols_by_theme['external_scores'],
                                    xlabel='Score (0-1)', sharex=True, kde=True)
"""

from .eda import histogram_per_group, frequency_per_group

__all__ = ["histogram_per_group", "frequency_per_group"]
