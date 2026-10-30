# 08 - Reshape: pivot, unstack, melt, crosstab

`answers/08_reshape/qNN.py` &nbsp;|&nbsp; check with: `grade 08` or `grade 08 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

**Read with:** McKinney ch 8 (reshaping and pivoting) and ch 10 (pivot tables and cross-tabulation).

## Long vs wide

```
 LONG (one row per fact)          WIDE (one row per year)
 year  rate_type  loans           year  Fixed  Variable
 2024  Fixed      2100    pivot   2024  2100   8250
 2024  Variable   8250   ------>  2025  1900  10444
 2025  Fixed      1900   <------
 2025  Variable  10444    melt / stack
```

| Long -> wide | Wide -> long |
|---|---|
| `df.pivot_table(index='year', columns='rate_type', values='x', aggfunc='sum')` | `df.melt(id_vars='year')` |
| `s.unstack()` (inner index level -> columns) | `df.stack()` (columns -> inner index level) |
| `df.pivot(index=..., columns=..., values=...)` (no aggregation, keys must be unique) | |
| `pd.crosstab(a, b)` counts; `normalize='index'` gives row shares | |

## Tips
- `fill_value=0` in `pivot_table` / `unstack` turns missing cells into 0.
- `margins=True` adds an `All` row and column.
- After a pivot, the columns have a name (`rate_type`). `df.columns.name = None` tidies it; `reset_index()`
  brings the row keys back as a column.
- Vintage curves, roll-rate matrices and score-band tables are all pivots. This chapter is the one to know cold.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans by origination year (rows) and `rate_type` (columns) with `pivot_table`. Return `year`, `Fixed`, `Variable`;
sorted by `year`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

`pd.crosstab` of `channel` (rows) by `rate_type` (columns) as **row percentages** rounded to 2 dp.
Return `channel`, `Fixed`, `Variable`; sorted by `channel`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

Group by origination year and `channel`, count, then `unstack` the channel (missing = 0). Return `year`, then one
column per channel in alphabetical order (`Branch`, `Broker`, `Digital`, `Mobile Lender`); sorted by `year`.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

Melt `dim_product[['product_id', 'max_lvr_pct', 'annual_fee']]` into long form. Return `product_id`, `variable`,
`value`; sorted by `product_id`, then `variable`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `dim_product`

### Q05 &nbsp; ★★ &nbsp; (core)

Total `original_amount` in **$ millions** (rounded to 1 dp) by origination year (rows) and `rate_type` (columns),
with `margins=True`. Return `year`, `Fixed`, `Variable`, `All`, with the years in order and the `All` row last.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Start from the year x `rate_type` count table (Q01), `stack` it back to long form and keep only cells with **more
than 2,000** loans. Return `year`, `rate_type`, `loans`; sorted by `year`, `rate_type`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q07 &nbsp; ★★ &nbsp; (core)

`ref_property_price_index` for 2025 month-ends: `pivot` so each row is a `month_end_date` and the columns are
`NSW` and `SA` (just those two states). Return `month_end_date`, `NSW`, `SA`; sorted by `month_end_date`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `ref_property_price_index`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

For **closed** loans: counts by `closure_reason` (rows) and `rate_type` (columns), missing = 0. Return
`closure_reason`, `Fixed`, `Variable`; sorted by `closure_reason`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`
