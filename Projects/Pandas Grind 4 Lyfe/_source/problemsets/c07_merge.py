from . import P

PRIMER = r"""
**Read with:** McKinney ch 8 (combining and merging datasets).

## merge = SQL join

```
 loan                      dim_product                 loan.merge(dim_product, on='product_id', how='left')
 loan_id  product_id       product_id  occupancy       loan_id  product_id  occupancy
 1        3                3           Owner Occ       1        3           Owner Occ
 2        5                5           Investment      2        5           Investment
 3        99               (no 99)                     3        99          NaN        <- kept by 'left'
```

| how | keeps |
|---|---|
| `'inner'` (default) | only keys on both sides |
| `'left'` | every left row |
| `'outer'` | everything |

## Three habits that prevent silent bugs

1. **Check the row count** before and after. A many-to-one lookup must not add rows.
2. **`validate='many_to_one'`** makes pandas raise an error if the right side has duplicate keys.
3. **`indicator=True`** adds a `_merge` column (`left_only` / `right_only` / `both`): the easy anti-join.

## Fan-out
If the right side has 2 rows for one key, the left row appears twice. A loan with two securities becomes
two rows, and any sum of loan amounts after the join is now **double counted**.

## Other joins
- Different column names: `left_on='primary_customer_id', right_on='customer_id'`.
- Two keys: `on=['application_id', 'customer_id']`.
- "Value in force at a date": `pd.merge_asof(left.sort_values('d'), right.sort_values('d2'), left_on='d', right_on='d2')`
  takes the last right row at or before each left date.
- Stacking tables with the same columns: `pd.concat([a, b])`.
"""

CONCEPT = dict(id="07_merge", title="07 - Merge, join and concat", primer=PRIMER, problems=[
    P(1, """
Bring `occupancy` from `dim_product` onto `loan` and count loans per occupancy. Return `occupancy`, `loans`;
sorted by `occupancy`.
""", """
m = loan.merge(dim_product[['product_id', 'occupancy']], on='product_id', how='left', validate='many_to_one')
result = m.groupby('occupancy').size()
""", ["loan", "dim_product"]),

    P(1, """
Join `app` to `assess` on `application_id` and return the median `nsr` for `'Approved'` and `'Declined'`
decisions, rounded to 3 dp. Return `decision`, `median_nsr`; sorted by `decision`.
""", """
m = app[['application_id', 'decision']].merge(assess[['application_id', 'nsr']], on='application_id')
result = m.groupby('decision')['nsr'].median().round(3)
""", ["loan_application", "application_assessment"], tol=0.0011),

    P(2, """
Anti-join: how many customers are **never** the `primary_customer_id` on a loan? (`indicator=True`)
""", """
m = customer[['customer_id']].merge(loan[['primary_customer_id']].drop_duplicates(),
                                    left_on='customer_id', right_on='primary_customer_id',
                                    how='left', indicator=True)
result = int((m['_merge'] == 'left_only').sum())
""", ["customer", "loan"]),

    P(2, """
Fan-out check. Join `loan` to `loan_security` on `loan_id` (inner). Return one row: `rows_before` (loans),
`rows_after` (rows after the join) and `amount_double_counted` = the sum of `original_amount` after the join
minus the true total, rounded to 0 dp.
""", """
m = loan[['loan_id', 'original_amount']].merge(loan_security[['loan_id', 'security_id']], on='loan_id')
result = pd.DataFrame({'rows_before': [len(loan)], 'rows_after': [len(m)],
                       'amount_double_counted': [round(m['original_amount'].sum() - loan['original_amount'].sum(), 0)]})
""", ["loan", "loan_security"]),

    P(2, """
Loans per **branch state** (join `dim_branch` on `branch_id` with `validate='many_to_one'`; loans with no branch
are left out). Return `state`, `loans`; sorted by `loans` (most first), then `state`.
""", """
b = loan.dropna(subset=['branch_id']).merge(dim_branch[['branch_id', 'state']], on='branch_id', validate='many_to_one')
result = (b.groupby('state').size().rename('loans').reset_index()
          .sort_values(['loans', 'state'], ascending=[False, True]))
""", ["loan", "dim_branch"]),

    P(2, """
The **primary** applicant's bureau score per application: join `applicant` (role `'Primary'`) to `bureau` on
**both** `application_id` and `customer_id`, then join `app` for the decision. Average `bureau_score` (thin files
excluded) per `decision`, rounded to 1 dp. Return `decision`, `avg_score`; sorted by `decision`.
""", """
prim = applicant.loc[applicant['applicant_role'] == 'Primary', ['application_id', 'customer_id']]
s = prim.merge(bureau[['application_id', 'customer_id', 'bureau_score']], on=['application_id', 'customer_id'])
s = s.merge(app[['application_id', 'decision']], on='application_id')
result = s.groupby('decision')['bureau_score'].mean().round(1)
""", ["application_applicant", "credit_bureau_report", "loan_application"]),

    P(3, """
For each loan, find the **RBA cash rate in force** at its `origination_date` (latest `bank_effective_date` on or
before it, `merge_asof`). Average spread = `interest_rate_at_origination_pct` minus `cash_rate_pct`, per origination
year, rounded to 3 dp. Return `year`, `avg_spread`; sorted by `year`.
""", """
l = loan[['loan_id', 'origination_date', 'interest_rate_at_origination_pct']].sort_values('origination_date')
r = ref_rba_cash_rate[['bank_effective_date', 'cash_rate_pct']].sort_values('bank_effective_date')
m = pd.merge_asof(l, r, left_on='origination_date', right_on='bank_effective_date')
m['spread'] = m['interest_rate_at_origination_pct'] - m['cash_rate_pct']
result = m.groupby(m['origination_date'].dt.year.rename('year'))['spread'].mean().round(3)
""", ["loan", "ref_rba_cash_rate"], tol=0.0011, hint="Both frames must be sorted by their date column before `merge_asof`."),

    P(3, """
Arrears bucket for each live loan at 2025-12-31 using `ref_arrears_bucket` (`merge_asof` on `days_past_due`
against `dpd_from`). Return `bucket_name`, `loans` for every bucket that has loans; sorted by `bucket_id`
(so in bucket order, not alphabetical).
""", """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]
l = live[['loan_id', 'days_past_due']].sort_values('days_past_due')
b = ref_arrears_bucket.sort_values('dpd_from')
m = pd.merge_asof(l, b, left_on='days_past_due', right_on='dpd_from')
result = (m.groupby(['bucket_id', 'bucket_name']).size().rename('loans').reset_index()
          .sort_values('bucket_id')[['bucket_name', 'loans']])
""", ["loan_monthly_snapshot", "ref_arrears_bucket"], order=True,
      hint="merge_asof needs both sides sorted, and int keys of the same type. Sort the result by bucket_id, then drop it."),

    P(2, """
Stack two small tables with `pd.concat`: loans per channel originated in 2024 and in 2025, in **long** form.
Return `year`, `channel`, `loans`; sorted by `year`, `channel`.
""", """
yr = loan['origination_date'].dt.year
parts = []
for y in [2024, 2025]:
    t = loan.loc[yr == y].groupby('channel').size().rename('loans').reset_index()
    t.insert(0, 'year', y)
    parts.append(t)
result = pd.concat(parts, ignore_index=True).sort_values(['year', 'channel'])
""", ["loan"]),
])
