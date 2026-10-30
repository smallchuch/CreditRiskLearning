# 03 - Selecting, filtering and sorting

`answers/03_selection/qNN.py` &nbsp;|&nbsp; check with: `grade 03` or `grade 03 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

The 5 largest loans by `original_amount`: return `loan_id`, `original_amount`; sorted by amount (largest
first), then `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q02 &nbsp; ★ &nbsp; (warm-up)

How many loans came through the `'Digital'` or `'Mobile Lender'` channels? (`isin`)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

### Q03 &nbsp; ★ &nbsp; (warm-up)

Share of loans by `rate_type`, as a percentage rounded to 2 dp. Return `rate_type`, `pct`; sorted by `rate_type`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q04 &nbsp; ★ &nbsp; (warm-up)

How many loans have `lvr_at_origination_pct` between 80 and 90 **inclusive**? (`between`)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

### Q05 &nbsp; ★★ &nbsp; (core)

Active loans (`loan_status == 'Active'`) with `lvr_at_origination_pct` above 98. Return `loan_id`,
`lvr_at_origination_pct`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **209 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`

### Q06 &nbsp; ★★ &nbsp; (core)

Sort `loan` by `original_amount` (largest first), then `loan_id`. What is the `loan_id` of the **100th** row (position 99)?

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `loan`

<details><summary>hint</summary>

After sorting, the index labels are scrambled, so this needs `iloc` (position), not `loc`.

</details>

### Q07 &nbsp; ★★ &nbsp; (core)

Products whose `product_name` contains the word `'Fixed'`. Return `product_id`, `product_name`, `fixed_term_months`;
sorted by `product_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `dim_product`

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Among **Variable**-rate loans originated in **2025**, the 10 with the highest `interest_rate_at_origination_pct`.
Return `loan_id`, `interest_rate_at_origination_pct`; sorted by rate (highest first), then `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `loan`
