from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="08_reshape", title="08 - Reshape: pivot, unstack, melt, crosstab", primer=PRIMER, problems=[
    P(1, """
Loans by origination year (rows) and `rate_type` (columns) with `pivot_table`. Return `year`, `Fixed`, `Variable`;
sorted by `year`.
""", """
t = loan.assign(year=loan['origination_date'].dt.year)
result = t.pivot_table(index='year', columns='rate_type', values='loan_id', aggfunc='count', fill_value=0)
""", ["loan"]),

    P(1, """
`pd.crosstab` of `channel` (rows) by `rate_type` (columns) as **row percentages** rounded to 2 dp.
Return `channel`, `Fixed`, `Variable`; sorted by `channel`.
""", """
result = (pd.crosstab(loan['channel'], loan['rate_type'], normalize='index') * 100).round(2)
""", ["loan"]),

    P(2, """
Group by origination year and `channel`, count, then `unstack` the channel (missing = 0). Return `year`, then one
column per channel in alphabetical order (`Branch`, `Broker`, `Digital`, `Mobile Lender`); sorted by `year`.
""", """
result = loan.groupby([loan['origination_date'].dt.year.rename('year'), 'channel']).size().unstack(fill_value=0)
""", ["loan"]),

    P(2, """
Melt `dim_product[['product_id', 'max_lvr_pct', 'annual_fee']]` into long form. Return `product_id`, `variable`,
`value`; sorted by `product_id`, then `variable`.
""", """
result = (dim_product[['product_id', 'max_lvr_pct', 'annual_fee']]
          .melt(id_vars='product_id').sort_values(['product_id', 'variable']))
""", ["dim_product"]),

    P(2, """
Total `original_amount` in **$ millions** (rounded to 1 dp) by origination year (rows) and `rate_type` (columns),
with `margins=True`. Return `year`, `Fixed`, `Variable`, `All`, with the years in order and the `All` row last.
""", """
t = loan.assign(year=loan['origination_date'].dt.year, amt_m=loan['original_amount'] / 1e6)
result = t.pivot_table(index='year', columns='rate_type', values='amt_m', aggfunc='sum', margins=True).round(1)
""", ["loan"], order=True),

    P(3, """
Start from the year x `rate_type` count table (Q01), `stack` it back to long form and keep only cells with **more
than 2,000** loans. Return `year`, `rate_type`, `loans`; sorted by `year`, `rate_type`.
""", """
t = loan.assign(year=loan['origination_date'].dt.year)
wide = t.pivot_table(index='year', columns='rate_type', values='loan_id', aggfunc='count', fill_value=0)
long = wide.stack().rename('loans').reset_index()
result = long[long['loans'] > 2000].sort_values(['year', 'rate_type'])
""", ["loan"]),

    P(2, """
`ref_property_price_index` for 2025 month-ends: `pivot` so each row is a `month_end_date` and the columns are
`NSW` and `SA` (just those two states). Return `month_end_date`, `NSW`, `SA`; sorted by `month_end_date`.
""", """
p = ref_property_price_index[ref_property_price_index['month_end_date'].dt.year == 2025]
result = p.pivot(index='month_end_date', columns='state', values='price_index')[['NSW', 'SA']]
""", ["ref_property_price_index"]),

    P(3, """
For **closed** loans: counts by `closure_reason` (rows) and `rate_type` (columns), missing = 0. Return
`closure_reason`, `Fixed`, `Variable`; sorted by `closure_reason`.
""", """
c = loan[loan['loan_status'] == 'Closed']
result = pd.crosstab(c['closure_reason'], c['rate_type'])
""", ["loan"]),
])
