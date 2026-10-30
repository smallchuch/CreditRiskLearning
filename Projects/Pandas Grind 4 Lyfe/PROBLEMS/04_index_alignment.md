# 04 - Index, labels and alignment

`answers/04_index_alignment/qNN.py` &nbsp;|&nbsp; check with: `grade 04` or `grade 04 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 5 ("Index objects", "Arithmetic and data alignment", "Reindexing").

## pandas matches by LABEL, not by position

```
 a = loans per purpose 2024      b = loans per purpose 2025       b - a
 Construction   500              Construction     450             Construction   -50
 Refinance     2600              Purchase - OO   4400             Purchase - OO   NaN  <- not in a
 Purchase - OO 4100              Refinance       2900             Refinance       300
```
Rows were in a different order and it still lined up, because pandas matched the labels.
A label missing on one side gives `NaN`; use `b.sub(a, fill_value=0)` to treat it as 0.

## Moving things between the index and the columns

| Want | Write |
|---|---|
| a column becomes the index | `df.set_index('loan_id')` |
| the index becomes a column | `df.reset_index()` |
| throw the index away | `df.reset_index(drop=True)` |
| rename the index | `s.rename_axis('channel')` |
| force a set of labels | `s.reindex([1, 2, 3], fill_value=0)` |

## Lookups with `.map`

```python
names = dim_product.set_index('product_id')['product_name']   # a Series used as a dictionary
loan['product_id'].map(names)                                 # label in -> value out
```

## Grouped results have a MultiIndex

```python
s = loan.groupby(['rate_type', 'channel']).size()
s.loc['Fixed']            # all channels for Fixed
s.unstack()               # second level becomes columns
```

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Using `set_index('loan_id')` and `.loc`, return the `original_amount` of loan 12345.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Loans per channel as a DataFrame with **columns** `channel`, `loans` (not an index). Sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

Let `a` = loans per `purpose` originated in 2024 and `b` = the same for 2025. Return `b - a` by purpose,
treating a purpose missing from one year as 0. Return `purpose`, `change`; sorted by `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

`b - a` already lines up by label. `fill_value=0` handles a label that is on only one side.

</details>

### Q04 &nbsp; ★★ &nbsp; (core)

Share of loans that are `'Closed'`, by channel, computed by **dividing two Series** (closed count / all
count) and letting pandas align them. Percentage rounded to 2 dp. Return `channel`, `pct_closed`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q05 &nbsp; ★★ &nbsp; (core)

Put loans per `purpose` for 2024 and 2025 **side by side** with `pd.concat(..., axis=1)`: columns
`purpose`, `n_2024`, `n_2025`, missing counts as 0. Sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q06 &nbsp; ★★ &nbsp; (core)

Add each loan's `product_name` with `.map` (a Series from `dim_product` used as a lookup), then count loans per
product name. Return `product_name`, `loans`; sorted by `loans` (most first), then `product_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`, `dim_product`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Count loans by `rate_type` and `channel` (a two-level index), then select just the `'Fixed'` part with `.loc`.
Return `channel`, `loans`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

New loans per calendar month of **2023** for the `'Construction'` purpose. Every month 1 to 12 must appear,
with 0 where there were none (`reindex`). Return `month`, `loans`; sorted by `month`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`
