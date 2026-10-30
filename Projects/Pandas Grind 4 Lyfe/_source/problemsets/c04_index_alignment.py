from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="04_index_alignment", title="04 - Index, labels and alignment", primer=PRIMER, problems=[
    P(1, """
Using `set_index('loan_id')` and `.loc`, return the `original_amount` of loan 12345.
""", """
result = loan.set_index('loan_id').loc[12345, 'original_amount']
""", ["loan"]),

    P(1, """
Loans per channel as a DataFrame with **columns** `channel`, `loans` (not an index). Sorted by `channel`.
""", """
result = loan['channel'].value_counts().rename_axis('channel').reset_index(name='loans').sort_values('channel')
""", ["loan"]),

    P(2, """
Let `a` = loans per `purpose` originated in 2024 and `b` = the same for 2025. Return `b - a` by purpose,
treating a purpose missing from one year as 0. Return `purpose`, `change`; sorted by `purpose`.
""", """
yr = loan['origination_date'].dt.year
a = loan.loc[yr == 2024, 'purpose'].value_counts()
b = loan.loc[yr == 2025, 'purpose'].value_counts()
result = b.sub(a, fill_value=0).rename_axis('purpose').sort_index()
""", ["loan"], hint="`b - a` already lines up by label. `fill_value=0` handles a label that is on only one side."),

    P(2, """
Share of loans that are `'Closed'`, by channel, computed by **dividing two Series** (closed count / all
count) and letting pandas align them. Percentage rounded to 2 dp. Return `channel`, `pct_closed`; sorted by `channel`.
""", """
closed = loan.loc[loan['loan_status'] == 'Closed', 'channel'].value_counts()
total = loan['channel'].value_counts()
result = (100 * closed / total).round(2).rename_axis('channel').sort_index()
""", ["loan"]),

    P(2, """
Put loans per `purpose` for 2024 and 2025 **side by side** with `pd.concat(..., axis=1)`: columns
`purpose`, `n_2024`, `n_2025`, missing counts as 0. Sorted by `purpose`.
""", """
yr = loan['origination_date'].dt.year
a = loan.loc[yr == 2024, 'purpose'].value_counts().rename('n_2024')
b = loan.loc[yr == 2025, 'purpose'].value_counts().rename('n_2025')
result = pd.concat([a, b], axis=1).fillna(0).rename_axis('purpose').sort_index()
""", ["loan"]),

    P(2, """
Add each loan's `product_name` with `.map` (a Series from `dim_product` used as a lookup), then count loans per
product name. Return `product_name`, `loans`; sorted by `loans` (most first), then `product_name`.
""", """
names = dim_product.set_index('product_id')['product_name']
counts = loan['product_id'].map(names).value_counts().rename_axis('product_name').reset_index(name='loans')
result = counts.sort_values(['loans', 'product_name'], ascending=[False, True])
""", ["loan", "dim_product"]),

    P(3, """
Count loans by `rate_type` and `channel` (a two-level index), then select just the `'Fixed'` part with `.loc`.
Return `channel`, `loans`; sorted by `channel`.
""", """
s = loan.groupby(['rate_type', 'channel']).size()
result = s.loc['Fixed'].sort_index()
""", ["loan"]),

    P(3, """
New loans per calendar month of **2023** for the `'Construction'` purpose. Every month 1 to 12 must appear,
with 0 where there were none (`reindex`). Return `month`, `loans`; sorted by `month`.
""", """
c = loan[(loan['purpose'] == 'Construction') & (loan['origination_date'].dt.year == 2023)]
result = c['origination_date'].dt.month.value_counts().reindex(range(1, 13), fill_value=0).rename_axis('month')
""", ["loan"]),
])
