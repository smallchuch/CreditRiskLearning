# ══════════════════════════════════════════════════════════════════════════════
# missingness_analysis.py
# Reusable missing data analysis script — drop this into any project
# ──────────────────────────────────────────────────────────────────────────────
# USAGE:
#   from missingness_analysis import run_missingness_report
#   run_missingness_report(df)
#
# Or run standalone with any CSV:
#   python missingness_analysis.py your_data.csv
#
# Requires: missingno, pandas, numpy, matplotlib, seaborn, scipy
#   pip install missingno
# ══════════════════════════════════════════════════════════════════════════════

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import missingno as msno
from scipy import stats

# ── Try to load your design system — falls back to defaults if not found ──────
try:
    sys.path.append(os.path.join(os.path.abspath('..'), 'Core Resources'))
    import python_style_util as psu
    psu.set_style()
    C_PRIMARY   = psu.p('purple', 500)
    C_SECONDARY = psu.p('cyan',   600)
    C_DANGER    = psu.p('red',    500)
    C_SAFE      = psu.p('green',  500)
    C_WATCH     = psu.p('yellow', 600)
    C_NEUTRAL   = psu.p('grey',   500)
    C_LIGHT     = psu.p('grey',   200)
    C_TEXT      = psu.p('grey',   800)
    FONT_HEAD   = psu.fonts['heading']
    FONT_BODY   = psu.fonts['body']
    FONT_MONO   = psu.fonts['mono']
    SIZE_TITLE  = psu.sizes['title']
    SIZE_BODY   = psu.sizes['body']
    SIZE_SMALL  = psu.sizes['small']
    SIZE_MONO   = psu.sizes['mono']
    USING_PSU   = True
except Exception:
    C_PRIMARY   = '#732DD9'
    C_SECONDARY = '#0DBDCE'
    C_DANGER    = '#E53935'
    C_SAFE      = '#91C46C'
    C_WATCH     = '#CEAA40'
    C_NEUTRAL   = '#7F7F7F'
    C_LIGHT     = '#EBEBEB'
    C_TEXT      = '#262626'
    FONT_HEAD   = 'Arial'
    FONT_BODY   = 'Arial'
    FONT_MONO   = 'Courier New'
    SIZE_TITLE  = 14
    SIZE_BODY   = 10
    SIZE_SMALL  = 9
    SIZE_MONO   = 9
    USING_PSU   = False


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 1 — SUMMARY TABLE
# ══════════════════════════════════════════════════════════════════════════════

def missing_summary(df):
    """
    Returns a summary DataFrame showing missing counts, percentages,
    dtype, and a simple missingness type hint for each column.
    """
    total     = len(df)
    missing   = df.isnull().sum()
    pct       = (missing / total * 100).round(2)
    dtype     = df.dtypes

    # Severity flag
    def severity(p):
        if p == 0:     return '✅ Complete'
        elif p < 5:    return '🟢 Low (<5%)'
        elif p < 20:   return '🟡 Moderate (5-20%)'
        elif p < 50:   return '🟠 High (20-50%)'
        else:          return '🔴 Critical (>50%)'

    summary = pd.DataFrame({
        'Missing Count': missing,
        'Missing %':     pct,
        'Dtype':         dtype,
        'Severity':      pct.apply(severity)
    }).sort_values('Missing %', ascending=False)

    return summary


def print_summary(df, dataset_name='Dataset'):
    """
    Print a clean text summary of missingness to the console / notebook.
    """
    summary = missing_summary(df)
    total   = len(df)
    n_cols_with_missing = (summary['Missing Count'] > 0).sum()
    total_cells  = df.size
    missing_cells = df.isnull().sum().sum()

    print("═" * 60)
    print(f"  MISSINGNESS REPORT — {dataset_name.upper()}")
    print("═" * 60)
    print(f"  Rows:              {total:,}")
    print(f"  Columns:           {len(df.columns):,}")
    print(f"  Total cells:       {total_cells:,}")
    print(f"  Missing cells:     {missing_cells:,} ({missing_cells/total_cells*100:.2f}%)")
    print(f"  Columns with NaNs: {n_cols_with_missing} of {len(df.columns)}")
    print("─" * 60)
    print(summary[summary['Missing Count'] > 0].to_string())
    print("═" * 60)

    return summary


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 2 — MISSINGNO VISUALISATIONS
# ══════════════════════════════════════════════════════════════════════════════

def plot_bar(df, dataset_name='Dataset'):
    """
    Missingno bar chart — shows completeness of each column as a bar.
    Good first look — instantly shows which columns have missing data.
    """
    fig, ax = plt.subplots(figsize=(12, 5))

    msno.bar(
        df,
        ax=ax,
        color=C_PRIMARY,
        fontsize=SIZE_SMALL,
        sort='ascending'
    )

    ax.set_title(
        f'Column Completeness — {dataset_name}',
        fontfamily=FONT_HEAD, fontsize=SIZE_TITLE,
        fontweight='bold', color=C_TEXT, loc='left', pad=12
    )
    ax.tick_params(labelsize=SIZE_SMALL)
    plt.tight_layout()
    plt.show()


def plot_matrix(df, dataset_name='Dataset'):
    """
    Missingno matrix — shows missingness patterns across rows.
    White = missing, dark = present.
    Look for horizontal white bands = rows with many missing values.
    Look for vertical white bands = columns almost entirely missing.
    Look for aligned patterns = missingness in one column correlates with another.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    msno.matrix(
        df,
        ax=ax,
        color=(0.447, 0.176, 0.851),   # purple 500 as RGB tuple
        fontsize=SIZE_SMALL,
        sparkline=True
    )

    ax.set_title(
        f'Missingness Matrix — {dataset_name}',
        fontfamily=FONT_HEAD, fontsize=SIZE_TITLE,
        fontweight='bold', color=C_TEXT, loc='left', pad=12
    )
    plt.tight_layout()
    plt.show()


def plot_heatmap(df, dataset_name='Dataset'):
    """
    Missingno heatmap — shows correlation between missingness across columns.
    High positive correlation = columns tend to be missing together.
    High negative correlation = when one is missing the other is present.
    Useful for identifying MNAR patterns.
    """
    cols_with_missing = df.columns[df.isnull().any()].tolist()

    if len(cols_with_missing) < 2:
        print("Heatmap requires at least 2 columns with missing values. Skipping.")
        return

    fig, ax = plt.subplots(figsize=(max(8, len(cols_with_missing)), max(6, len(cols_with_missing) * 0.8)))

    msno.heatmap(
        df[cols_with_missing],
        ax=ax,
        fontsize=SIZE_SMALL,
        cmap='RdYlGn'
    )

    ax.set_title(
        f'Missingness Correlation Heatmap — {dataset_name}\n'
        f'Green = missing together | Red = inversely missing',
        fontfamily=FONT_HEAD, fontsize=SIZE_TITLE,
        fontweight='bold', color=C_TEXT, loc='left', pad=12
    )
    plt.tight_layout()
    plt.show()


def plot_dendrogram(df, dataset_name='Dataset'):
    """
    Missingno dendrogram — clusters columns by similarity of missingness pattern.
    Columns grouped close together have similar missing patterns.
    Useful for identifying which features have linked missingness — potential MNAR signal.
    """
    cols_with_missing = df.columns[df.isnull().any()].tolist()

    if len(cols_with_missing) < 2:
        print("Dendrogram requires at least 2 columns with missing values. Skipping.")
        return

    fig, ax = plt.subplots(figsize=(12, 5))

    msno.dendrogram(
        df,
        ax=ax,
        fontsize=SIZE_SMALL,
        orientation='top'
    )

    ax.set_title(
        f'Missingness Dendrogram — {dataset_name}\n'
        f'Columns clustered by similarity of missingness pattern',
        fontfamily=FONT_HEAD, fontsize=SIZE_TITLE,
        fontweight='bold', color=C_TEXT, loc='left', pad=12
    )
    plt.tight_layout()
    plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 3 — MISSINGNESS TYPE ANALYSIS (MCAR / MAR / MNAR)
# ══════════════════════════════════════════════════════════════════════════════

def create_missingness_map(df):
    """
    Creates a binary dataframe — 1 where value is missing, 0 where present.
    Used as the foundation for MCAR/MAR/MNAR analysis.
    """
    return df.isnull().astype(int)


def plot_missingness_correlation_heatmap(df, dataset_name='Dataset'):
    """
    Spearman correlation heatmap between missingness indicators and original values.
    Based on the TDS article approach.

    Interpretation:
    - Red (positive) = missingness in that column correlates with higher values
      in another column → suggests MAR or MNAR
    - Blue (negative) = missingness correlates with lower values → suggests MAR
    - White/grey = no correlation → consistent with MCAR
    """
    cols_with_missing = df.columns[df.isnull().any()].tolist()

    if len(cols_with_missing) == 0:
        print("No missing values found. Skipping missingness correlation heatmap.")
        return

    mis_map = create_missingness_map(df)

    # Only compute for numeric columns in original data
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) == 0:
        print("No numeric columns found for correlation analysis.")
        return

    correlation_matrix = pd.DataFrame(
        index=cols_with_missing,
        columns=numeric_cols,
        dtype=float
    )

    for mis_col in cols_with_missing:
        for col in numeric_cols:
            if mis_col != col:
                try:
                    corr, _ = stats.spearmanr(
                        mis_map[mis_col],
                        df[col],
                        nan_policy='omit'
                    )
                    correlation_matrix.loc[mis_col, col] = corr
                except Exception:
                    correlation_matrix.loc[mis_col, col] = np.nan

    correlation_matrix = correlation_matrix.astype(float)

    fig_h = max(6, len(cols_with_missing) * 0.7)
    fig_w = max(10, len(numeric_cols) * 0.8)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))

    sns.heatmap(
        correlation_matrix,
        ax=ax,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        vmin=-1, vmax=1,
        linewidths=0.5,
        linecolor=C_LIGHT,
        annot_kws={'size': SIZE_MONO, 'family': FONT_MONO}
    )

    ax.set_title(
        f'Missingness vs Value Correlation — {dataset_name}\n'
        f'Rows = columns with missing data | Cols = numeric variables\n'
        f'Red = missing when value is HIGH (potential MNAR) | Blue = missing when value is LOW',
        fontfamily=FONT_HEAD, fontsize=SIZE_TITLE,
        fontweight='bold', color=C_TEXT, loc='left', pad=12
    )
    ax.set_xlabel('Original Data Columns', fontfamily=FONT_BODY, fontsize=SIZE_BODY)
    ax.set_ylabel('Missingness Indicators', fontfamily=FONT_BODY, fontsize=SIZE_BODY)
    ax.tick_params(labelsize=SIZE_SMALL)
    plt.tight_layout()
    plt.show()


def plot_missing_by_target(df, target_col, dataset_name='Dataset'):
    """
    For each column with missing values, compare the distribution of the
    target variable between rows where data IS missing vs IS present.

    If the target distribution differs significantly between missing/present
    groups → strong signal of MAR or MNAR (missingness is informative).
    If distributions are similar → consistent with MCAR.

    Only runs if target_col exists and is binary (0/1).
    """
    if target_col not in df.columns:
        print(f"Target column '{target_col}' not found. Skipping target analysis.")
        return

    cols_with_missing = df.columns[df.isnull().any()].tolist()
    cols_with_missing = [c for c in cols_with_missing if c != target_col]

    if len(cols_with_missing) == 0:
        print("No missing columns to analyse against target.")
        return

    n_cols = len(cols_with_missing)
    n_rows = (n_cols + 2) // 3
    fig, axes = plt.subplots(n_rows, 3, figsize=(14, n_rows * 4))
    axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes.flatten()

    for i, col in enumerate(cols_with_missing):
        ax = axes[i]

        missing_mask    = df[col].isnull()
        target_missing  = df.loc[missing_mask,  target_col]
        target_present  = df.loc[~missing_mask, target_col]

        # Default rate in each group
        rate_missing = target_missing.mean()
        rate_present = target_present.mean()

        bars = ax.bar(
            ['Data Present', 'Data Missing'],
            [rate_present, rate_missing],
            color=[C_SAFE, C_DANGER],
            edgecolor='white',
            width=0.5
        )

        # Value labels
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.005,
                f'{bar.get_height():.1%}',
                ha='center', va='bottom',
                fontfamily=FONT_MONO, fontsize=SIZE_MONO,
                color=C_TEXT
            )

        ax.set_title(
            col,
            fontfamily=FONT_HEAD, fontsize=SIZE_BODY,
            fontweight='bold', color=C_TEXT
        )
        ax.set_ylabel(f'{target_col} rate', fontfamily=FONT_BODY, fontsize=SIZE_SMALL)
        ax.set_ylim(0, max(rate_missing, rate_present) * 1.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(labelsize=SIZE_SMALL)

        # Flag if rates differ significantly
        diff = abs(rate_missing - rate_present)
        if diff > 0.05:
            ax.set_facecolor('#FFF8F8')
            ax.annotate(
                f'⚠ Δ{diff:.1%} — investigate',
                xy=(0.5, 0.95), xycoords='axes fraction',
                ha='center', va='top',
                fontsize=SIZE_SMALL, color=C_DANGER,
                fontfamily=FONT_BODY
            )

    # Hide unused axes
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    fig.suptitle(
        f'Default Rate by Missingness Status — {dataset_name}\n'
        f'If bars differ significantly → missingness may be informative (MAR/MNAR)',
        fontfamily=FONT_HEAD, fontsize=SIZE_TITLE,
        fontweight='bold', color=C_TEXT, y=1.01
    )
    plt.tight_layout()
    plt.show()


# ══════════════════════════════════════════════════════════════════════════════
# SECTION 4 — RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════

def print_recommendations(df):
    """
    Print actionable handling recommendations based on missingness percentage.
    These are starting points — always apply domain knowledge.
    """
    summary = missing_summary(df)
    missing_only = summary[summary['Missing Count'] > 0]

    if len(missing_only) == 0:
        print("✅ No missing values found — no action required.")
        return

    print("\n" + "═" * 60)
    print("  RECOMMENDED HANDLING STRATEGIES")
    print("  (Starting points — always apply domain knowledge)")
    print("═" * 60)

    for col, row in missing_only.iterrows():
        pct   = row['Missing %']
        dtype = str(row['Dtype'])
        is_numeric = 'int' in dtype or 'float' in dtype

        print(f"\n  📋 {col}  ({pct:.1f}% missing)")

        if pct > 50:
            print(f"     🔴 >50% missing — consider DROPPING this column")
            print(f"        Unless missingness itself is predictive (add indicator first)")
        elif pct > 20:
            print(f"     🟠 20-50% missing — HIGH missingness")
            print(f"        1. Add binary missing indicator column FIRST")
            if is_numeric:
                print(f"        2. Impute with MEDIAN (robust to skew)")
            else:
                print(f"        2. Impute with MODE or 'Unknown' category")
            print(f"        3. Consider whether MNAR — missingness may be signal")
        elif pct > 5:
            print(f"     🟡 5-20% missing — MODERATE")
            print(f"        1. Add binary missing indicator column")
            if is_numeric:
                print(f"        2. Impute with MEDIAN for skewed, MEAN for symmetric")
            else:
                print(f"        2. Impute with MODE")
        else:
            print(f"     🟢 <5% missing — LOW")
            if is_numeric:
                print(f"        Safe to impute with MEDIAN — low impact on distribution")
            else:
                print(f"        Safe to impute with MODE")

    print("\n" + "═" * 60)
    print("  REMINDER: Always fit imputer on TRAINING DATA ONLY")
    print("  Use sklearn Pipeline to prevent data leakage")
    print("═" * 60 + "\n")


# ══════════════════════════════════════════════════════════════════════════════
# MASTER FUNCTION — run everything
# ══════════════════════════════════════════════════════════════════════════════

def run_missingness_report(df, dataset_name='Dataset', target_col=None):
    """
    Run the complete missingness analysis pipeline on any DataFrame.

    Parameters:
    ───────────
    df           : pandas DataFrame
    dataset_name : str — label for chart titles
    target_col   : str or None — if provided, plots default rate by missingness status
                   Pass your binary target column name e.g. 'default' or 'target'

    Usage:
    ──────
    run_missingness_report(df, dataset_name='German Credit', target_col='default')
    """

    print(f"\n{'═'*60}")
    print(f"  RUNNING MISSINGNESS REPORT — {dataset_name.upper()}")
    print(f"{'═'*60}\n")

    # ── 1. Text summary ───────────────────────────────────────────
    print("── 1. SUMMARY TABLE ─────────────────────────────────────\n")
    summary = print_summary(df, dataset_name)

    # ── 2. Bar chart ──────────────────────────────────────────────
    print("\n── 2. COLUMN COMPLETENESS BAR CHART ─────────────────────")
    print("   Each bar shows % of non-missing values per column\n")
    plot_bar(df, dataset_name)

    # ── 3. Matrix ─────────────────────────────────────────────────
    print("\n── 3. MISSINGNESS MATRIX ────────────────────────────────")
    print("   White = missing | Dark = present")
    print("   Look for: aligned white bands = correlated missingness\n")
    plot_matrix(df, dataset_name)

    # ── 4. Missingno heatmap ──────────────────────────────────────
    cols_missing = df.columns[df.isnull().any()].tolist()
    if len(cols_missing) >= 2:
        print("\n── 4. MISSINGNO CORRELATION HEATMAP ─────────────────────")
        print("   Correlation between missingness patterns across columns\n")
        plot_heatmap(df, dataset_name)

        # ── 5. Dendrogram ─────────────────────────────────────────
        print("\n── 5. DENDROGRAM ────────────────────────────────────────")
        print("   Clusters columns by similarity of missingness pattern\n")
        plot_dendrogram(df, dataset_name)

        # ── 6. Missingness vs value correlation ───────────────────
        print("\n── 6. MISSINGNESS VS VALUE CORRELATION ──────────────────")
        print("   Red = missing when value HIGH (possible MNAR)")
        print("   Blue = missing when value LOW\n")
        plot_missingness_correlation_heatmap(df, dataset_name)
    else:
        print("\n   Skipping heatmap, dendrogram and correlation —")
        print("   fewer than 2 columns have missing values\n")

    # ── 7. Target analysis ────────────────────────────────────────
    if target_col:
        print(f"\n── 7. MISSINGNESS VS TARGET ({target_col.upper()}) ──────────────────")
        print("   Does default rate differ between missing/present groups?")
        print("   Big difference = missingness is informative (MAR/MNAR)\n")
        plot_missing_by_target(df, target_col, dataset_name)

    # ── 8. Recommendations ────────────────────────────────────────
    print("\n── 8. HANDLING RECOMMENDATIONS ──────────────────────────")
    print_recommendations(df)

    print("  ✅ Report complete.\n")

    return summary


# ══════════════════════════════════════════════════════════════════════════════
# STANDALONE USAGE — python missingness_analysis.py your_data.csv
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python missingness_analysis.py <path_to_csv> [target_column]")
        print("Example: python missingness_analysis.py german_credit.csv default")
        sys.exit(1)

    filepath    = sys.argv[1]
    target_col  = sys.argv[2] if len(sys.argv) > 2 else None
    dataset_name = os.path.basename(filepath).replace('.csv', '')

    df = pd.read_csv(filepath)
    run_missingness_report(df, dataset_name=dataset_name, target_col=target_col)