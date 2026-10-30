from . import P

PRIMER = r"""
**Read with:** McKinney ch 5 (Series and DataFrame basics, indexing with loc / iloc, sorting).

## loc = by label, iloc = by position

```
          loan_id  amount            df.loc[42, 'amount']   -> the row whose index LABEL is 42
 index                               df.iloc[0, 1]          -> first row, second column (POSITION)
   17       101    286000            df.loc[mask, ['loan_id', 'amount']]  -> rows where mask is True
   42       102    209000
   58       103    512000
```
After filtering, the index keeps its old labels (17, 42, 58 ...). That's why `iloc[0]` and `loc[0]`
can be completely different rows.

## Filtering

| Want | Write |
|---|---|
| one condition | `df[df['x'] > 5]` |
| several | `df[(df['x'] > 5) & (df['y'] == 'A')]` |
| in a list | `df[df['channel'].isin(['Digital', 'Mobile Lender'])]` |
| a range (inclusive) | `df[df['lvr'].between(80, 90)]` |
| text match | `df[df['name'].str.contains('Fixed')]` |
| select columns too | `df.loc[mask, ['a', 'b']]` |

## Sorting and top-N

```python
df.sort_values(['amount', 'loan_id'], ascending=[False, True])   # ties broken by the 2nd column
df.nlargest(5, 'amount')
s.value_counts(normalize=True)   # shares instead of counts
```
"""

CONCEPT = dict(id="03_selection", title="03 - Selecting, filtering and sorting", primer=PRIMER, problems=[
    P(1, """
The 5 largest loans by `original_amount`: return `loan_id`, `original_amount`; sorted by amount (largest
first), then `loan_id`.
""", """
result = loan.sort_values(['original_amount', 'loan_id'], ascending=[False, True]).head(5)[['loan_id', 'original_amount']]
""", ["loan"]),

    P(1, """
How many loans came through the `'Digital'` or `'Mobile Lender'` channels? (`isin`)
""", """
result = int(loan['channel'].isin(['Digital', 'Mobile Lender']).sum())
""", ["loan"]),

    P(1, """
Share of loans by `rate_type`, as a percentage rounded to 2 dp. Return `rate_type`, `pct`; sorted by `rate_type`.
""", """
result = (loan['rate_type'].value_counts(normalize=True) * 100).round(2).sort_index()
""", ["loan"]),

    P(1, """
How many loans have `lvr_at_origination_pct` between 80 and 90 **inclusive**? (`between`)
""", """
result = int(loan['lvr_at_origination_pct'].between(80, 90).sum())
""", ["loan"]),

    P(2, """
Active loans (`loan_status == 'Active'`) with `lvr_at_origination_pct` above 98. Return `loan_id`,
`lvr_at_origination_pct`; sorted by `loan_id`.
""", """
mask = (loan['loan_status'] == 'Active') & (loan['lvr_at_origination_pct'] > 98)
result = loan.loc[mask, ['loan_id', 'lvr_at_origination_pct']].sort_values('loan_id')
""", ["loan"]),

    P(2, """
Sort `loan` by `original_amount` (largest first), then `loan_id`. What is the `loan_id` of the **100th** row (position 99)?
""", """
result = int(loan.sort_values(['original_amount', 'loan_id'], ascending=[False, True]).iloc[99]['loan_id'])
""", ["loan"], hint="After sorting, the index labels are scrambled, so this needs `iloc` (position), not `loc`."),

    P(2, """
Products whose `product_name` contains the word `'Fixed'`. Return `product_id`, `product_name`, `fixed_term_months`;
sorted by `product_id`.
""", """
result = dim_product.loc[dim_product['product_name'].str.contains('Fixed'),
                         ['product_id', 'product_name', 'fixed_term_months']].sort_values('product_id')
""", ["dim_product"]),

    P(3, """
Among **Variable**-rate loans originated in **2025**, the 10 with the highest `interest_rate_at_origination_pct`.
Return `loan_id`, `interest_rate_at_origination_pct`; sorted by rate (highest first), then `loan_id`.
""", """
mask = (loan['rate_type'] == 'Variable') & (loan['origination_date'].dt.year == 2025)
cols = ['loan_id', 'interest_rate_at_origination_pct']
result = (loan.loc[mask, cols]
          .sort_values(['interest_rate_at_origination_pct', 'loan_id'], ascending=[False, True])
          .head(10))
""", ["loan"]),
])
