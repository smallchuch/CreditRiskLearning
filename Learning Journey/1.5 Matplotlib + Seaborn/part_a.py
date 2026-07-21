# Part A: title, setup, matplotlib fundamentals (sections 1-9)
# Each cell is ("md", text) or ("code", text)

CELLS_A = []

CELLS_A.append(("md", '''# Matplotlib & Seaborn Practice — Home Credit Default Risk

A full practice workbook covering the matplotlib and seaborn skills you need for credit risk EDA, built on `application_train.csv`.

**How to use this notebook**

1. Work through sections in order — matplotlib fundamentals first, then seaborn, then a capstone.
2. Each section gives you brief context and the key syntax, then exercises. Write your code in the empty cells.
3. Every section also has **interpretation questions** — answer them in the markdown cells provided. Saying what a plot *shows* and what it *means for credit risk* is the skill that separates an analyst from a chart-maker.
4. Bring your attempts to Claude for marking, or ask for hints when stuck. Try each exercise cold first.

**Ground rules**

- Every plot gets a title and axis labels. No exceptions — build the habit now.
- Before running each plot, predict what it will look like (hypothesis-before-analysis).
- If a plot surprises you, that is a finding. Write it down.
'''))

# ---------------- Section 0: Setup ----------------
CELLS_A.append(("md", '''## 0 — Setup and data loading

Run these cells to get started. The load cell follows your usual repo-relative pattern — adjust `DATA_PATH` if your data lives elsewhere.
'''))

CELLS_A.append(("code", '''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

pd.set_option("display.max_columns", 130)
print("matplotlib:", plt.matplotlib.__version__)
print("seaborn:", sns.__version__)'''))

CELLS_A.append(("code", '''from pathlib import Path

def find_repo_root(marker=".git"):
    p = Path.cwd()
    for parent in [p, *p.parents]:
        if (parent / marker).exists():
            return parent
    return p

REPO_ROOT = find_repo_root()
# Adjust this to wherever application_train.csv sits in your repo:
DATA_PATH = REPO_ROOT / "Data" / "home-credit-default-risk" / "application_train.csv"

df = pd.read_csv(DATA_PATH)
print(df.shape)'''))

CELLS_A.append(("md", '''### Derived columns

The `DAYS_*` columns are negative day counts relative to the application date, which makes for unreadable axes. Create clean versions once here and use them throughout.

**Exercise 0.1** — Create the following columns:

- `AGE_YEARS` — age in years from `DAYS_BIRTH` (positive, in years)
- `YEARS_EMPLOYED` — from `DAYS_EMPLOYED` (positive, in years). Do **not** clean the anomaly yet — a later exercise depends on it being dirty.
- `CREDIT_INCOME_RATIO` — `AMT_CREDIT / AMT_INCOME_TOTAL`
- `ANNUITY_INCOME_RATIO` — `AMT_ANNUITY / AMT_INCOME_TOTAL`

Then print `df[["AGE_YEARS", "YEARS_EMPLOYED"]].describe()` and look at the max of `YEARS_EMPLOYED`.

**Interpretation 0.1** — What do you notice about the maximum of `YEARS_EMPLOYED`? What do you suspect it encodes, and why would a lender's system produce a value like that?
'''))

CELLS_A.append(("code", '''# Ex 0.1 — derived columns
'''))

CELLS_A.append(("md", '''**Your answer (0.1):**

...
'''))

# ---------------- Section 1: Anatomy of a figure ----------------
CELLS_A.append(("md", '''## 1 — Anatomy of a figure

Matplotlib has two APIs: the quick **pyplot** interface (`plt.plot(...)`) and the **object-oriented (OO)** interface (`fig, ax = plt.subplots()` then `ax.plot(...)`). The OO interface is the one to build muscle memory on — it scales to multi-panel figures and is what serious EDA code uses.

The object hierarchy:

- **Figure** — the whole canvas. Owns one or more Axes.
- **Axes** — one plot (the thing with an x-axis and y-axis). This is where 95% of your method calls go.
- **Axis** — the x or y axis object itself (ticks, limits, labels).
- **Artist** — everything drawn (lines, patches, text) is an Artist.

**Key syntax**

```python
fig, ax = plt.subplots(figsize=(8, 5))   # one Figure, one Axes
ax.plot(x, y)                            # draw on the Axes
ax.set_title("Title")
ax.set_xlabel("x label")
ax.set_ylabel("y label")
plt.show()
```

### Exercises

**1.1** — Using the OO interface, make a simple line plot of `y = x**2` for `x = np.arange(0, 10)`. Title it and label both axes. (Yes, it is a toy — the point is the API pattern.)

**1.2** — Same plot, but written with the pyplot interface (`plt.plot`, `plt.title`, ...). Confirm you get the same output.

**Interpretation 1.1** — In your own words: what is the difference between the Figure and the Axes? Why does the OO interface matter once you start building 2×2 comparison panels for an EDA report?

**Interpretation 1.2** — When you see `plt.gca()` in someone else's code, what is it doing?
'''))

CELLS_A.append(("code", '''# Ex 1.1 — OO interface
'''))

CELLS_A.append(("code", '''# Ex 1.2 — pyplot interface
'''))

CELLS_A.append(("md", '''**Your answers (1.1, 1.2):**

...
'''))

# ---------------- Section 2: Line plots ----------------
CELLS_A.append(("md", '''## 2 — Line plots and basic styling

Line plots show how a value changes across an ordered variable. In credit risk you rarely plot raw rows as lines — you plot **aggregates**: default rate by age band, approval volume by month, rate by score decile.

**Key syntax**

```python
ax.plot(x, y,
        color="tab:blue",      # named colours, hex, or "C0".."C9"
        linestyle="--",        # "-", "--", ":", "-."
        linewidth=2,
        marker="o",            # add point markers
        label="series name")   # picked up by ax.legend()
ax.legend()
```

### Exercises

**2.1** — Compute the mean of `TARGET` grouped by `HOUR_APPR_PROCESS_START` (this is the default rate by hour the application was started). Plot it as a line with circle markers. Title, labels, and a legend entry.

**2.2** — Add a second line to the same Axes: the **number of applications** per hour. Wait — that has a totally different scale. For now, plot it anyway and observe the problem. (Section 8 fixes this properly with a twin axis.)

**2.3** — Restyle 2.1: dashed red line, linewidth 2, square markers. Purely a syntax rep.

**Interpretation 2.1** — Describe the default-rate-by-hour pattern. What might explain applications started at unusual hours having different risk? Would you trust the hours with very few applications?

**Interpretation 2.2** — Why is plotting two very different scales on one axis misleading? What are the two standard fixes?
'''))

CELLS_A.append(("code", '''# Ex 2.1 — default rate by application hour
'''))

CELLS_A.append(("code", '''# Ex 2.2 — add application volume (observe the scale problem)
'''))

CELLS_A.append(("code", '''# Ex 2.3 — restyle
'''))

CELLS_A.append(("md", '''**Your answers (2.1, 2.2):**

...
'''))

# ---------------- Section 3: Histograms ----------------
CELLS_A.append(("md", '''## 3 — Histograms

The workhorse of univariate EDA. In credit risk you histogram incomes, loan amounts, ages, and scores to find skew, outliers, data-entry artefacts, and sentinel values before they poison a model.

**Key syntax**

```python
ax.hist(series.dropna(), bins=50,
        edgecolor="white",     # visible bin borders
        alpha=0.7,
        density=True)          # normalise to a density instead of counts
ax.hist(a, bins=bins, alpha=0.5, label="A")   # overlay two with shared bins
bins = np.linspace(lo, hi, 41)                # explicit shared bin edges
```

### Exercises

**3.1** — Histogram of `AGE_YEARS` with 40 bins. Then re-run with 5 bins and 200 bins. Keep all three (separate cells or a loop).

**3.2** — Histogram of `AMT_INCOME_TOTAL`. It will look terrible. Diagnose why, then fix it two ways: (a) clip/filter to below the 99th percentile, (b) keep all data but pass `np.log10` of income. Plot both.

**3.3** — Overlay the `AGE_YEARS` distributions for defaulters (`TARGET == 1`) and non-defaulters (`TARGET == 0`) on one Axes. Use `density=True`, shared explicit bins, `alpha=0.5`, and a legend. This is the single most important histogram pattern in this dataset — you will reuse it constantly.

**3.4** — Histogram of `YEARS_EMPLOYED` (still dirty). Find the anomaly visually, then create `YEARS_EMPLOYED_CLEAN` where the sentinel is replaced with `np.nan`, and re-plot.

**Interpretation 3.1** — What did 5 bins hide and what did 200 bins invent? How do you choose?

**Interpretation 3.2** — Why is `density=True` essential in 3.3 when the two groups have very different sizes? What would raw counts mislead you into thinking?

**Interpretation 3.3** — From 3.3: which age groups default more? Give a plausible economic explanation, and one policy implication a lender might (carefully, legally) consider.

**Interpretation 3.4** — What does the `DAYS_EMPLOYED` sentinel most likely represent? Why replace with NaN rather than 0 or the median at the EDA stage?
'''))

CELLS_A.append(("code", '''# Ex 3.1 — AGE_YEARS histograms, three bin counts
'''))

CELLS_A.append(("code", '''# Ex 3.2 — income histogram, then two fixes
'''))

CELLS_A.append(("code", '''# Ex 3.3 — age distribution by TARGET (density, shared bins)
'''))

CELLS_A.append(("code", '''# Ex 3.4 — find and clean the YEARS_EMPLOYED sentinel
'''))

CELLS_A.append(("md", '''**Your answers (3.1–3.4):**

...
'''))

# ---------------- Section 4: Bar charts ----------------
CELLS_A.append(("md", '''## 4 — Bar charts

Bars compare quantities across categories: default rate by education, counts by income type. Rule of thumb — **horizontal bars** (`barh`) whenever category names are long, and **sort the bars** unless the category has a natural order.

**Key syntax**

```python
counts = df["COL"].value_counts()
rates = df.groupby("COL")["TARGET"].mean().sort_values()

ax.bar(counts.index, counts.values)
ax.barh(rates.index, rates.values)             # horizontal
ax.tick_params(axis="x", rotation=45)          # or use barh instead

# grouped bars: shift positions by width
x = np.arange(len(labels)); w = 0.4
ax.bar(x - w/2, series_a, width=w, label="A")
ax.bar(x + w/2, series_b, width=w, label="B")
ax.set_xticks(x, labels)
```

### Exercises

**4.1** — Vertical bar chart of application counts by `NAME_INCOME_TYPE`. Rotate the x labels so they are readable.

**4.2** — Horizontal bar chart of **default rate** by `NAME_EDUCATION_TYPE`, sorted ascending. Add a vertical reference line at the overall default rate (`df["TARGET"].mean()`).

**4.3** — Grouped bar chart: for `CODE_GENDER` (drop the XNA row), show two bars per gender — count of non-defaulters and count of defaulters. Legend required.

**4.4** — Default rate by `OCCUPATION_TYPE`, horizontal, sorted, with the overall-rate reference line. There are ~18 categories — this is exactly when `barh` earns its keep.

**Interpretation 4.1** — From 4.2: which education levels sit above the portfolio-average default rate? Is the pattern monotonic with education? Why might education correlate with default even though no lender prices on education directly?

**Interpretation 4.2** — In 4.3, why is a *grouped count* chart nearly useless for comparing risk between genders? What chart answers the risk question directly?

**Interpretation 4.3** — From 4.4: name the two highest-risk and two lowest-risk occupations. What income-stability story connects them?
'''))

CELLS_A.append(("code", '''# Ex 4.1 — counts by income type
'''))

CELLS_A.append(("code", '''# Ex 4.2 — default rate by education, sorted, with reference line
'''))

CELLS_A.append(("code", '''# Ex 4.3 — grouped bars by gender and target
'''))

CELLS_A.append(("code", '''# Ex 4.4 — default rate by occupation
'''))

CELLS_A.append(("md", '''**Your answers (4.1–4.3):**

...
'''))

# ---------------- Section 5: Scatter plots ----------------
CELLS_A.append(("md", '''## 5 — Scatter plots

Scatters show the joint distribution of two numerics. With 307k rows, naive scatters become solid ink blobs — the skill here is **overplotting management**: sampling, alpha, and colour mapping.

**Key syntax**

```python
sample = df.sample(5000, random_state=42)
ax.scatter(x, y,
           s=8,                # marker size
           alpha=0.2,          # transparency fights overplotting
           c=values,           # colour by a third variable
           cmap="viridis")
fig.colorbar(sc, ax=ax, label="third variable")   # sc = the scatter handle
```

### Exercises

**5.1** — Scatter `AMT_CREDIT` (y) vs `AMT_GOODS_PRICE` (x) on a 5,000-row sample. First with defaults, then tuned (`s=8, alpha=0.2`). Note the structure you can see.

**5.2** — Scatter `AMT_CREDIT` vs `AMT_INCOME_TOTAL` on a sample, colouring points by `TARGET` (two colours — plot the two groups as two `scatter` calls so you get a proper legend). Filter income to below the 99th percentile first.

**5.3** — Scatter `EXT_SOURCE_2` (x) vs `EXT_SOURCE_3` (y) on a sample, coloured by `AGE_YEARS` with a continuous colormap and a colorbar.

**Interpretation 5.1** — In 5.1 you should see points hugging a line, plus banding. What is the credit vs goods-price relationship telling you about how these loans are structured? What causes the banding?

**Interpretation 5.2** — Can you visually separate defaulters from non-defaulters in 5.2? What does that tell you about how useful raw income and credit amount will be as standalone model features?

**Interpretation 5.3** — The EXT_SOURCE columns are external credit scores. From 5.3, are the two scores correlated? Does age appear related to either? Why do normalised external scores so often end up as the strongest features in this competition?
'''))

CELLS_A.append(("code", '''# Ex 5.1 — credit vs goods price
'''))

CELLS_A.append(("code", '''# Ex 5.2 — credit vs income coloured by TARGET
'''))

CELLS_A.append(("code", '''# Ex 5.3 — EXT_SOURCE_2 vs EXT_SOURCE_3 coloured by age
'''))

CELLS_A.append(("md", '''**Your answers (5.1–5.3):**

...
'''))

# ---------------- Section 6: Customisation ----------------
CELLS_A.append(("md", '''## 6 — Customisation: ticks, formatters, grids, spines

Default matplotlib output says "draft". Formatted ticks, a light grid, and removed top/right spines say "report". These few lines are most of the difference.

**Key syntax**

```python
ax.set_xlim(20, 70); ax.set_ylim(0, 0.12)
ax.grid(axis="y", alpha=0.3)
ax.spines[["top", "right"]].set_visible(False)

# tick formatting
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0))   # 0.08 -> 8%
ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))  # 1,000,000
ax.xaxis.set_major_locator(mticker.MultipleLocator(5))             # tick every 5

fig.suptitle("Figure-level title", fontsize=14)
fig.tight_layout()
```

### Exercises

**6.1** — Rebuild your 4.2 chart (default rate by education) with: percent-formatted value axis, light grid on the value axis only, top and right spines removed, and a proper title stating the takeaway (a "headline title", e.g. "Lower secondary education carries the highest default rate" rather than "Default rate by education").

**6.2** — Rebuild 3.2's clipped income histogram with thousands-separator x ticks and spines removed.

**6.3** — Take your 3.3 age-by-target overlay and set x limits to the actual age range (roughly 20–70), add `MultipleLocator(5)` x ticks, and a grid.

**Interpretation 6.1** — Why are headline titles better than descriptive titles in a report for a credit committee? Give one situation where a neutral descriptive title is the right choice instead.
'''))

CELLS_A.append(("code", '''# Ex 6.1 — polished education chart
'''))

CELLS_A.append(("code", '''# Ex 6.2 — polished income histogram
'''))

CELLS_A.append(("code", '''# Ex 6.3 — polished age overlay
'''))

CELLS_A.append(("md", '''**Your answer (6.1):**

...
'''))

# ---------------- Section 7: Annotations ----------------
CELLS_A.append(("md", '''## 7 — Annotations and reference lines

Annotations turn a chart into an argument: mark the portfolio average, flag the anomaly, label the number that matters.

**Key syntax**

```python
ax.axhline(0.08, color="red", linestyle="--", label="portfolio avg")
ax.axvline(threshold, color="grey", linestyle=":")
ax.axvspan(60, 70, alpha=0.15, color="orange")        # shaded band

ax.text(x, y, "label", ha="center", va="bottom")
ax.annotate("sentinel value",
            xy=(x_point, y_point),          # arrow tip
            xytext=(x_text, y_text),        # text position
            arrowprops=dict(arrowstyle="->"))

# value labels on bars
for bar in bars:
    ax.text(bar.get_width(), bar.get_y() + bar.get_height()/2,
            f" {bar.get_width():.1%}", va="center")
```

### Exercises

**7.1** — Take the 4.4 occupation chart and add a percentage value label at the end of each bar.

**7.2** — Histogram of the *raw* `DAYS_EMPLOYED` (all data, before cleaning) and use `ax.annotate` with an arrow to point at the sentinel spike, labelled with what you concluded it means.

**7.3** — On your 2.1 default-rate-by-hour line, shade the band of hours you consider "out of business hours" with `axvspan`, and add an `axhline` at the overall default rate.

**Interpretation 7.1** — Annotation is persuasive. What is the risk of over-annotating, or of annotating only the points that support your prior? How would you keep yourself honest?
'''))

CELLS_A.append(("code", '''# Ex 7.1 — bar value labels
'''))

CELLS_A.append(("code", '''# Ex 7.2 — annotate the sentinel
'''))

CELLS_A.append(("code", '''# Ex 7.3 — shaded band + reference line
'''))

CELLS_A.append(("md", '''**Your answer (7.1):**

...
'''))

# ---------------- Section 8: Scales and twin axes ----------------
CELLS_A.append(("md", '''## 8 — Log scales and twin axes

Money variables are right-skewed almost by definition — a handful of very large incomes crush the rest of the axis. Log scales fix that. Twin axes solve the two-different-units problem from Exercise 2.2 (use sparingly; they are easy to abuse).

**Key syntax**

```python
ax.set_xscale("log")          # log the axis (keeps original units on ticks)
ax.hist(np.log10(series))     # vs transforming the data itself

ax2 = ax.twinx()              # second y-axis sharing the same x
ax2.plot(x, y2, color="tab:orange")
ax2.set_ylabel("second unit")
```

### Exercises

**8.1** — Histogram of `AMT_INCOME_TOTAL` (all rows, no clipping) with `ax.set_xscale("log")`. Compare mentally with your 3.2 approaches.

**8.2** — Fix Exercise 2.2 properly: default rate by hour as a line on the left axis (percent-formatted), application volume per hour as bars on a twin right axis (drawn first, in a light colour, so the line stays readable). Label both axes clearly.

**8.3** — Boxplot-free skew check: plot `.plot(kind="hist")`-style histograms of `CREDIT_INCOME_RATIO` on linear and log x scales side by side in one figure (peek at Section 9 for `plt.subplots(1, 2)`).

**Interpretation 8.1** — When presenting to a non-technical credit committee, what is the danger of a log axis? How would you caption it?

**Interpretation 8.2** — In 8.2, which hours have high default rates but tiny volume? Why should the volume context change how much you trust — and how you would act on — the rate line?
'''))

CELLS_A.append(("code", '''# Ex 8.1 — log-scale income
'''))

CELLS_A.append(("code", '''# Ex 8.2 — rate line + volume bars on twin axes
'''))

CELLS_A.append(("code", '''# Ex 8.3 — linear vs log side by side
'''))

CELLS_A.append(("md", '''**Your answers (8.1, 8.2):**

...
'''))

# ---------------- Section 9: Subplots and saving ----------------
CELLS_A.append(("md", '''## 9 — Subplot layouts and saving figures

Multi-panel figures are the format of real EDA output: one figure, four related views, one takeaway. This is where the OO interface pays off.

**Key syntax**

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].hist(...)                   # index the 2D array of Axes
for ax, col in zip(axes.flat, cols):   # or iterate over axes.flat
    ax.hist(df[col].dropna(), bins=40)
    ax.set_title(col)

fig, axes = plt.subplots(1, 2, sharey=True)   # shared axis limits
fig.suptitle("One overall title")
fig.tight_layout()

fig.savefig("figure.png", dpi=150, bbox_inches="tight")
```

### Exercises

**9.1** — A 2×2 grid of histograms for `AMT_INCOME_TOTAL` (clipped), `AMT_CREDIT`, `AMT_ANNUITY`, `AMT_GOODS_PRICE`. Loop over `axes.flat` rather than writing four blocks. Each panel titled; one `suptitle`.

**9.2** — A 1×3 grid: distributions of `EXT_SOURCE_1`, `EXT_SOURCE_2`, `EXT_SOURCE_3`, each split by TARGET (your 3.3 overlay pattern), with `sharey=True`.

**9.3** — Save the 9.2 figure as a PNG at `dpi=150` with `bbox_inches="tight"`, then confirm the file exists.

**Interpretation 9.1** — From 9.2: rank the three external sources by how well they visually separate defaulters from non-defaulters. What does "separation" in a density overlay correspond to in model terms?

**Interpretation 9.2** — Why `sharey=True` when comparing the three panels? What comparison would be corrupted without it?
'''))

CELLS_A.append(("code", '''# Ex 9.1 — 2x2 money histograms
'''))

CELLS_A.append(("code", '''# Ex 9.2 — EXT_SOURCE panels by TARGET
'''))

CELLS_A.append(("code", '''# Ex 9.3 — savefig
'''))

CELLS_A.append(("md", '''**Your answers (9.1, 9.2):**

...
'''))
