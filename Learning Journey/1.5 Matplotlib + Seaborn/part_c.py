# Part C: capstone + wrap-up

CELLS_C = []

CELLS_C.append(("md", '''## 17 — Capstone: a one-figure risk dashboard

Everything above, combined. Build **one figure** you could drop into a portfolio README or hand to a credit manager. No new syntax — this is composition, polish, and judgement.

**The brief**

Build a 2×2 figure, `figsize=(14, 10)`, titled with a headline finding, containing:

1. **Top-left** — default rate by `NAME_EDUCATION_TYPE`: horizontal bars, sorted, percent axis, portfolio-average reference line, value labels.
2. **Top-right** — `EXT_SOURCE_3` density by TARGET (`histplot`, `hue`, `stat="density"`, `common_norm=False`, `element="step"`).
3. **Bottom-left** — default rate by 5-year age band: compute with `pd.cut` on `AGE_YEARS`, then plot as a line with markers, percent axis. (Bonus: add faint volume bars on a twin axis.)
4. **Bottom-right** — the 14.1 correlation heatmap (or a trimmed version), masked upper triangle.

Requirements: consistent styling across panels (`set_theme` once), every panel titled, spines handled, `tight_layout` or `constrained_layout`, saved to PNG at 150 dpi.

**Then write the analysis** (markdown cell below): four decision statements, one per panel, in your agreed format — *observation → decision*. Example shape: "Default rate falls monotonically with age from ~12% (20–25) to ~5% (60+) → retain AGE_YEARS as a model feature; consider banded version for scorecard interpretability."
'''))

CELLS_C.append(("code", '''# Capstone — build the dashboard here
# (feel free to develop each panel in its own scratch cell first, then assemble)
'''))

CELLS_C.append(("md", '''**Capstone decision statements:**

Panel 1 (education):

Panel 2 (EXT_SOURCE_3):

Panel 3 (age bands):

Panel 4 (correlations):
'''))

CELLS_C.append(("md", '''## 18 — Self-test: can you answer these cold?

Close the notebook docs. If any of these are shaky, redo the relevant section.

1. Figure vs Axes — one sentence each.
2. The three lines that turn a draft chart into a report chart.
3. When you must use `common_norm=False`, and what goes wrong without it.
4. Axes-level vs figure-level seaborn functions — and which one accepts `ax=`.
5. What `sns.barplot(x=cat, y="TARGET")` estimates, and what the whiskers are.
6. Boxplot vs violin — what each shows and hides.
7. Why a diverging colormap for correlations and a sequential one for rates.
8. Three ways to handle overplotting in a 300k-row scatter.
9. Why you check group sizes before quoting subgroup default rates.
10. The `DAYS_EMPLOYED` sentinel: what it is, how you found it, what you did about it.

**When you're done:** bring your completed sections to Claude for marking — plots and written answers both. Then this feeds straight into finishing the Home Credit EDA with decision statements.
'''))
