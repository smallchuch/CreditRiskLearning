# Part B: seaborn sections 10-16

CELLS_B = []

# ---------------- Section 10: Seaborn intro ----------------
CELLS_B.append(("md", '''## 10 — Seaborn: how it relates to matplotlib

Seaborn is a layer on top of matplotlib: it takes a DataFrame plus column names, handles grouping/aggregation/legends for you, and draws using matplotlib underneath. Everything you learned in Sections 1–9 still applies — most seaborn functions return or draw onto a matplotlib `Axes`, so you polish seaborn plots with the same `ax.set_*` calls.

The one distinction that prevents 90% of seaborn confusion:

- **Axes-level functions** (`sns.histplot`, `sns.boxplot`, `sns.scatterplot`, `sns.heatmap`, ...) draw on a single Axes. They accept `ax=` and slot into `plt.subplots` grids.
- **Figure-level functions** (`sns.displot`, `sns.catplot`, `sns.relplot`, `sns.lmplot`, `sns.jointplot`, `sns.pairplot`) create their **own figure** (a `FacetGrid`). They do NOT accept `ax=` — you cannot put them inside your own subplot grid, but they can facet into columns/rows on their own.

**Key syntax**

```python
sns.set_theme(style="whitegrid")           # opt in to seaborn styling

fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(data=df, x="AGE_YEARS", ax=ax)   # axes-level: composable
ax.set_title("still plain matplotlib methods")

sns.displot(data=df, x="AGE_YEARS", col="TARGET")   # figure-level: own figure
```

### Exercises

**10.1** — Call `sns.set_theme(style="whitegrid")`. Re-run one of your Section 3 histograms unchanged and note what changed visually.

**10.2** — Draw `sns.histplot(data=df, x="AGE_YEARS")` into an Axes you created with `plt.subplots`, and set the title with matplotlib. Then try passing `ax=` to `sns.displot` and read the warning/error you get.

**Interpretation 10.1** — In your own words: when would you reach for the axes-level function and when for the figure-level one? Which will you use inside a 2×2 EDA panel?
'''))

CELLS_B.append(("code", '''# Ex 10.1 — set_theme, re-run an old plot
'''))

CELLS_B.append(("code", '''# Ex 10.2 — axes-level vs figure-level
'''))

CELLS_B.append(("md", '''**Your answer (10.1):**

...
'''))

# ---------------- Section 11: Distributions ----------------
CELLS_B.append(("md", '''## 11 — Distribution plots: histplot, kdeplot, ecdfplot

Seaborn's distribution tools do in one line what took you several in Section 3 — especially splitting by a grouping variable with `hue`. In this dataset, `hue="TARGET"` is the move you will make hundreds of times.

**Key syntax**

```python
sns.histplot(data=df, x="COL", hue="TARGET",
             stat="density",        # like density=True
             common_norm=False,     # CRITICAL: normalise each group separately
             element="step",        # cleaner overlays than bars
             bins=50, ax=ax)

sns.kdeplot(data=df, x="COL", hue="TARGET", common_norm=False,
            fill=True, alpha=0.3, ax=ax)

sns.ecdfplot(data=df, x="COL", hue="TARGET", ax=ax)
```

### Exercises

**11.1** — Redo your 3.3 age-by-target overlay in ONE `sns.histplot` call using `hue`, `stat="density"`, `common_norm=False`, `element="step"`. Compare effort with your matplotlib version.

**11.2** — Run the same plot but with `common_norm=True` (the default). Observe how the defaulter distribution almost vanishes.

**11.3** — `sns.kdeplot` of `EXT_SOURCE_3` by TARGET, filled. Then the same variable as `sns.ecdfplot` by TARGET.

**11.4** — KDE of `AMT_CREDIT` by TARGET with `log_scale=True`. (Yes, `log_scale` is built in.)

**Interpretation 11.1** — Explain precisely what `common_norm=False` does and why it is essential with an ~8%/92% class imbalance. What lie does `common_norm=True` tell here?

**Interpretation 11.2** — KDE vs histogram: what does the KDE smooth over, and when is that smoothing dangerous? (Hint: think about your sentinel spike and hard boundaries like age 21.)

**Interpretation 11.3** — Read the ECDF from 11.3: roughly what fraction of *defaulters* have `EXT_SOURCE_3` below 0.4, vs non-defaulters? Why are ECDFs the honest choice for comparing groups (no bins, no bandwidth)?
'''))

CELLS_B.append(("code", '''# Ex 11.1 — histplot with hue
'''))

CELLS_B.append(("code", '''# Ex 11.2 — common_norm=True (observe the problem)
'''))

CELLS_B.append(("code", '''# Ex 11.3 — kdeplot and ecdfplot of EXT_SOURCE_3
'''))

CELLS_B.append(("code", '''# Ex 11.4 — log-scale KDE of credit amount
'''))

CELLS_B.append(("md", '''**Your answers (11.1–11.3):**

...
'''))

# ---------------- Section 12: Categorical plots ----------------
CELLS_B.append(("md", '''## 12 — Categorical plots: countplot, barplot, boxplot, violinplot, stripplot

The categorical family answers "how does a numeric differ across groups" and "how big is each group". Know what each estimates:

- `countplot` — row counts per category (a `value_counts` bar chart)
- `barplot` — the **mean** of y per category, with a bootstrap confidence interval. With a 0/1 target, the mean IS the default rate — so `sns.barplot(x=cat, y="TARGET")` gives default rate with error bars for free.
- `boxplot` — median, quartiles, whiskers, outliers
- `violinplot` — full KDE shape per group
- `stripplot`/`swarmplot` — raw points (sample first!)

**Key syntax**

```python
sns.countplot(data=df, y="NAME_INCOME_TYPE",
              order=df["NAME_INCOME_TYPE"].value_counts().index, ax=ax)

sns.barplot(data=df, x="NAME_EDUCATION_TYPE", y="TARGET",
            order=[...], errorbar=("ci", 95), ax=ax)   # mean of 0/1 = default rate

sns.boxplot(data=df, x="TARGET", y="AGE_YEARS", ax=ax)
sns.violinplot(data=df, x="TARGET", y="EXT_SOURCE_2", ax=ax)
sns.violinplot(..., hue="CODE_GENDER", split=True)     # split violins
```

### Exercises

**12.1** — `countplot` of `NAME_FAMILY_STATUS`, horizontal, ordered by frequency.

**12.2** — `barplot` of default rate by `NAME_EDUCATION_TYPE` with 95% CIs, ordered by rate. Compare with your hand-built 4.2: what did you get for free?

**12.3** — `boxplot` of `AMT_INCOME_TOTAL` by `TARGET`. Diagnose why it is unreadable, then fix (filter extreme incomes or log scale).

**12.4** — `violinplot` of `EXT_SOURCE_2` by `TARGET`. Then a split violin: `x="TARGET"`, `y="AGE_YEARS"`, `hue="CODE_GENDER"` (drop XNA), `split=True`.

**12.5** — `stripplot` of `AMT_ANNUITY` by `NAME_CONTRACT_TYPE` on a 2,000-row sample with `alpha=0.3`. Optionally overlay a boxplot on the same Axes.

**12.6** — Default rate by `REGION_RATING_CLIENT` as a barplot. Note this category is ordinal (1, 2, 3) — keep the natural order.

**Interpretation 12.1** — In 12.2, the CI whiskers are wide for some education levels and narrow for others. What drives the width, and how should it affect your confidence in the rate ranking?

**Interpretation 12.2** — Boxes vs violins: what did the violin in 12.4 reveal about `EXT_SOURCE_2` that the five-number summary of a boxplot compresses away?

**Interpretation 12.3** — Does `REGION_RATING_CLIENT` behave monotonically with default? Why does monotonicity matter if you later want to use a feature in a scorecard-style (logistic) model?

**Interpretation 12.4** — Median incomes for defaulters vs non-defaulters are close. Why can a variable with near-identical group medians still be useful in a model?
'''))

CELLS_B.append(("code", '''# Ex 12.1 — countplot family status
'''))

CELLS_B.append(("code", '''# Ex 12.2 — barplot default rate by education with CIs
'''))

CELLS_B.append(("code", '''# Ex 12.3 — income boxplot, diagnose and fix
'''))

CELLS_B.append(("code", '''# Ex 12.4 — violins and split violins
'''))

CELLS_B.append(("code", '''# Ex 12.5 — stripplot on a sample
'''))

CELLS_B.append(("code", '''# Ex 12.6 — default rate by region rating
'''))

CELLS_B.append(("md", '''**Your answers (12.1–12.4):**

...
'''))

# ---------------- Section 13: Relational + regression ----------------
CELLS_B.append(("md", '''## 13 — Relational and regression plots: scatterplot, regplot, lmplot, jointplot

Seaborn's `scatterplot` adds `hue`/`size`/`style` semantics to what you built manually in Section 5. `regplot` overlays a fitted regression line; `jointplot` glues a scatter to marginal distributions.

**Key syntax**

```python
sns.scatterplot(data=sample, x="A", y="B",
                hue="TARGET", alpha=0.3, s=15, ax=ax)

sns.regplot(data=sample, x="A", y="B",
            scatter_kws=dict(alpha=0.2, s=10),
            line_kws=dict(color="red"), ax=ax)

sns.jointplot(data=sample, x="A", y="B", kind="scatter")   # figure-level
# kind: "scatter", "hex", "kde", "hist", "reg"

sns.lmplot(data=sample, x="A", y="B", hue="TARGET")        # figure-level regplot
```

### Exercises

**13.1** — Redo 5.2 (credit vs income, coloured by TARGET) as a single `sns.scatterplot` with `hue`. One line plus polish.

**13.2** — `regplot` of `AMT_ANNUITY` vs `AMT_CREDIT` on a 5,000-row sample. Style the scatter faint and the line red.

**13.3** — `jointplot` of `EXT_SOURCE_2` vs `EXT_SOURCE_3` on a sample, `kind="hex"`. Try `kind="kde"` too.

**13.4** — `lmplot` of `AMT_ANNUITY` vs `AMT_CREDIT` with `hue="NAME_CONTRACT_TYPE"` on a sample. Two fitted lines.

**Interpretation 13.1** — The annuity–credit relationship in 13.2 is nearly deterministic. What does an annuity actually represent (you know this from mortgage lending), and why is `AMT_ANNUITY / AMT_CREDIT` roughly the same for loans of the same term?

**Interpretation 13.2** — In 13.4, cash loans and revolving loans show different annuity-per-credit slopes. What does that reflect about the two products?

**Interpretation 13.3** — When is fitting a straight line (`regplot`) actively misleading? Name a check you would run before trusting it.
'''))

CELLS_B.append(("code", '''# Ex 13.1 — scatterplot with hue
'''))

CELLS_B.append(("code", '''# Ex 13.2 — regplot annuity vs credit
'''))

CELLS_B.append(("code", '''# Ex 13.3 — jointplot hex / kde
'''))

CELLS_B.append(("code", '''# Ex 13.4 — lmplot by contract type
'''))

CELLS_B.append(("md", '''**Your answers (13.1–13.3):**

...
'''))

# ---------------- Section 14: Heatmaps ----------------
CELLS_B.append(("md", '''## 14 — Heatmaps: correlations, crosstabs, missingness

`sns.heatmap` renders any 2-D matrix as colour. In credit EDA the big three uses are correlation matrices, category×category rate tables, and missingness patterns.

**Key syntax**

```python
corr = df[num_cols].corr()
sns.heatmap(corr,
            annot=True, fmt=".2f",       # print values in the cells
            cmap="coolwarm",
            vmin=-1, vmax=1, center=0,   # anchor the diverging colormap
            square=True, ax=ax)

mask = np.triu(np.ones_like(corr, dtype=bool))   # hide the duplicate triangle
sns.heatmap(corr, mask=mask, ...)

pivot = df.pivot_table(index="CAT_A", columns="CAT_B",
                       values="TARGET", aggfunc="mean")
sns.heatmap(pivot, annot=True, fmt=".1%", cmap="Reds", ax=ax)
```

### Exercises

**14.1** — Correlation heatmap of: `TARGET`, `AGE_YEARS`, `YEARS_EMPLOYED_CLEAN`, `AMT_INCOME_TOTAL`, `AMT_CREDIT`, `AMT_ANNUITY`, `AMT_GOODS_PRICE`, `EXT_SOURCE_1`, `EXT_SOURCE_2`, `EXT_SOURCE_3`, `CREDIT_INCOME_RATIO`. Annotated, `coolwarm`, centred at 0, upper triangle masked.

**14.2** — Default-rate pivot heatmap: `NAME_EDUCATION_TYPE` (rows) × `NAME_FAMILY_STATUS` (columns), values = mean TARGET, annotated as percentages, `cmap="Reds"`. Also produce the corresponding **count** pivot so you know which cells are thin.

**14.3** — Missingness heatmap: take ~20 columns spanning low and high missingness (include the EXT_SOURCEs and some building columns like `EXT_SOURCE_1`, `OWN_CAR_AGE`, `OCCUPATION_TYPE`, and a few `*_AVG` columns), build `df[cols].isna()`, and heatmap a 2,000-row sample of it (`cbar=False`, no annot).

**Interpretation 14.1** — From 14.1: which feature has the strongest (absolute) correlation with TARGET, and is it positive or negative? Why are all the target correlations small in magnitude, and why does that NOT mean the features are useless?

**Interpretation 14.2** — `AMT_CREDIT`, `AMT_ANNUITY`, and `AMT_GOODS_PRICE` form a highly correlated block. What problem does that cause for a logistic regression, and name two ways to deal with it.

**Interpretation 14.3** — From 14.2 + the count pivot: find one cell with an extreme rate. Is it trustworthy? What minimum-count rule would you apply before quoting cell-level rates to stakeholders?

**Interpretation 14.4** — From 14.3: does missingness look random, or do columns go missing together in blocks? What does block-missingness usually indicate about how the data was collected, and how does it change your imputation strategy?
'''))

CELLS_B.append(("code", '''# Ex 14.1 — correlation heatmap with mask
'''))

CELLS_B.append(("code", '''# Ex 14.2 — education x family status default-rate pivot (+ counts)
'''))

CELLS_B.append(("code", '''# Ex 14.3 — missingness heatmap
'''))

CELLS_B.append(("md", '''**Your answers (14.1–14.4):**

...
'''))

# ---------------- Section 15: Multi-plot grids ----------------
CELLS_B.append(("md", '''## 15 — Faceting: catplot, displot, relplot, FacetGrid, pairplot

Faceting = same plot, repeated across subsets ("small multiples"). The figure-level functions (`catplot`, `displot`, `relplot`) are the front doors; `FacetGrid` is the engine underneath; `pairplot` is a grid of pairwise scatters.

**Key syntax**

```python
sns.displot(data=df, x="AGE_YEARS", hue="TARGET",
            col="NAME_CONTRACT_TYPE",      # one column of panels per category
            stat="density", common_norm=False, element="step")

sns.catplot(data=df, x="TARGET", y="EXT_SOURCE_2",
            col="CODE_GENDER", kind="violin")

sns.relplot(data=sample, x="AMT_GOODS_PRICE", y="AMT_CREDIT",
            col="NAME_INCOME_TYPE", col_wrap=3, alpha=0.3)

sns.pairplot(sample[cols + ["TARGET"]], hue="TARGET",
             corner=True, plot_kws=dict(alpha=0.3, s=10))
```

### Exercises

**15.1** — `displot`: age distribution by TARGET (hue), faceted into columns by `NAME_CONTRACT_TYPE`.

**15.2** — `catplot`: violins of `EXT_SOURCE_2` by TARGET, faceted by `CODE_GENDER` (drop XNA first).

**15.3** — `relplot`: credit vs goods price scatter on a sample, faceted by `NAME_INCOME_TYPE` with `col_wrap=3`.

**15.4** — `pairplot` of the three EXT_SOURCE columns + `AGE_YEARS` on a 3,000-row sample, `hue="TARGET"`, `corner=True`. This is the money plot for this dataset.

**Interpretation 15.1** — From 15.1: does the age–risk relationship look the same for cash loans and revolving loans? If a relationship changes across facets, what does that imply for modelling (name the term)?

**Interpretation 15.2** — From 15.4: which single variable, or pair of variables, best separates the classes? Where in the grid do you look to answer "would a linear boundary work"?

**Interpretation 15.3** — Faceting into small subsets shrinks the data per panel. What is the trade-off, and when would you facet vs use hue on one Axes?
'''))

CELLS_B.append(("code", '''# Ex 15.1 — displot facets
'''))

CELLS_B.append(("code", '''# Ex 15.2 — catplot violins by gender
'''))

CELLS_B.append(("code", '''# Ex 15.3 — relplot col_wrap
'''))

CELLS_B.append(("code", '''# Ex 15.4 — pairplot of EXT_SOURCEs + age
'''))

CELLS_B.append(("md", '''**Your answers (15.1–15.3):**

...
'''))

# ---------------- Section 16: Palettes, themes, contexts ----------------
CELLS_B.append(("md", '''## 16 — Themes, palettes, contexts

Three independent dials:

- **style** — background/grid look: `whitegrid`, `darkgrid`, `ticks`, `white`
- **palette** — colours. The type must match the data type:
  - *qualitative* (categories): `"colorblind"`, `"tab10"`, `"Set2"`
  - *sequential* (low→high): `"viridis"`, `"Blues"`, `"rocket"`
  - *diverging* (negative↔positive around a midpoint): `"coolwarm"`, `"vlag"`, `"RdBu"`
- **context** — scaling for the medium: `paper`, `notebook` (default), `talk`, `poster`

**Key syntax**

```python
sns.set_theme(style="ticks", palette="colorblind", context="talk")
sns.color_palette("viridis", 8)          # inspect a palette in Jupyter
sns.histplot(..., palette="Set2")        # per-plot override (with hue)
sns.despine()                            # remove top/right spines
```

### Exercises

**16.1** — Display three palettes in-notebook with `sns.color_palette(...)`: one qualitative, one sequential, one diverging.

**16.2** — Re-render your 14.1 correlation heatmap with `cmap="viridis"`. It will look plausible and be wrong. Then switch back to a diverging map centred at 0.

**16.3** — Take one favourite plot from earlier and render it twice: `context="paper"` vs `context="talk"`.

**Interpretation 16.1** — Explain why a sequential colormap on a correlation matrix is a genuine error, not a style preference. What question can a reader not answer with viridis on [-1, 1]?

**Interpretation 16.2** — Why default to colorblind-safe palettes for anything a credit committee will see?
'''))

CELLS_B.append(("code", '''# Ex 16.1 — three palettes
'''))

CELLS_B.append(("code", '''# Ex 16.2 — wrong then right heatmap colormap
'''))

CELLS_B.append(("code", '''# Ex 16.3 — paper vs talk context
'''))

CELLS_B.append(("md", '''**Your answers (16.1, 16.2):**

...
'''))
