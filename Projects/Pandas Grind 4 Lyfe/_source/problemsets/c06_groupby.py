from . import P

PRIMER = r"""
**Read with:** McKinney ch 10 (GroupBy mechanics, aggregation, apply / transform).

## split -> apply -> combine

```
 loan rows                   split by channel          apply mean         combine
 channel  amount             Branch: 400k, 600k  ->     500k              channel  mean
 Branch   400k               Broker: 300k        ->     300k              Branch   500k
 Broker   300k                                                            Broker   300k
 Branch   600k
```
The group keys end up in the **index** of the result. `.reset_index()` (or `as_index=False`) turns them into columns.

## The four shapes of aggregation

| Write | Get |
|---|---|
| `df.groupby('k')['x'].mean()` | Series, one number per group |
| `df.groupby('k').size()` | rows per group (counts missing too) |
| `df.groupby('k')['x'].count()` | non-missing `x` per group |
| `df.groupby('k').agg(loans=('x', 'size'), avg=('x', 'mean'))` | named columns: the tidy way |

## transform: a group number on every row

```
 channel  amount   mean by channel (transform)   amount - mean
 Branch   400k     500k                          -100k
 Branch   600k     500k                          +100k
 Broker   300k     300k                             0
```
`df.groupby('k')['x'].transform('mean')` keeps the original row count, so you can compare each row with its group.

## Weighted average (credit risk staple)
`(x * w).sum() / w.sum()` per group. In a groupby, build `x * w` as a column first, then sum both and divide.

## Other everyday moves
`.filter(lambda g: len(g) > 200)` keeps whole groups; `.nlargest`, `.idxmax()` find the top row;
`sort_values(...).groupby(...).head(1)` = top row per group.
"""

CONCEPT = dict(id="06_groupby", title="06 - GroupBy: aggregate, transform, filter", primer=PRIMER, problems=[
    P(1, """
Number of loans per `purpose`. Return `purpose`, `loans`; sorted by `loans` (most first), then `purpose`.
""", """
result = (loan.groupby('purpose').size().rename('loans').reset_index()
          .sort_values(['loans', 'purpose'], ascending=[False, True]))
""", ["loan"]),

    P(1, """
Average `original_amount` per `channel`, rounded to 0 dp. Return `channel`, `avg_amount`; sorted by `channel`.
""", """
result = loan.groupby('channel')['original_amount'].mean().round(0)
""", ["loan"]),

    P(1, """
Per `rate_type`, with named aggregation: `loans` (count), `total_amount` (sum of `original_amount`, rounded to 0 dp)
and `avg_lvr` (mean `lvr_at_origination_pct`, rounded to 2 dp). Return `rate_type`, `loans`, `total_amount`, `avg_lvr`;
sorted by `rate_type`.
""", """
result = loan.groupby('rate_type').agg(loans=('loan_id', 'size'),
                                       total_amount=('original_amount', 'sum'),
                                       avg_lvr=('lvr_at_origination_pct', 'mean'))
result['total_amount'] = result['total_amount'].round(0)
result['avg_lvr'] = result['avg_lvr'].round(2)
""", ["loan"]),

    P(2, """
Live book at 2025-12-31 (`snapshot_date` = 2025-12-31, `loan_status` not `'Closed'`): the **balance-weighted**
average `interest_rate_pct` per `repayment_type`, rounded to 3 dp. Return `repayment_type`, `wavg_rate`; sorted by `repayment_type`.
""", """
live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')].copy()
live['rate_x_bal'] = live['interest_rate_pct'] * live['closing_balance']
g = live.groupby('repayment_type')[['rate_x_bal', 'closing_balance']].sum()
result = (g['rate_x_bal'] / g['closing_balance']).round(3)
""", ["loan_monthly_snapshot"], tol=0.0011),

    P(2, """
Loans per origination year and `rate_type`. Return `year`, `rate_type`, `loans`; sorted by `year`, `rate_type`.
""", """
result = loan.groupby([loan['origination_date'].dt.year.rename('year'), 'rate_type']).size()
""", ["loan"]),

    P(2, """
For each loan, compare `original_amount` with the **average for its channel** (`transform`). Per channel, how many
loans are above their channel average? Return `channel`, `above_avg`; sorted by `channel`.
""", """
avg = loan.groupby('channel')['original_amount'].transform('mean')
result = (loan['original_amount'] > avg).groupby(loan['channel']).sum()
""", ["loan"]),

    P(2, """
Brokers (`broker_id`, broker-channel loans) that wrote **more than 250** loans. Return `broker_id` (as an int),
`loans`; sorted by `loans` (most first), then `broker_id`.
""", """
b = loan.dropna(subset=['broker_id']).copy()
b['broker_id'] = b['broker_id'].astype(int)
n = b.groupby('broker_id').size().rename('loans').reset_index()
result = n[n['loans'] > 250].sort_values(['loans', 'broker_id'], ascending=[False, True])
""", ["loan"]),

    P(2, """
`size()` vs `count()`: per channel, the number of rows and the number with a `branch_id`. Return `channel`, `rows`,
`with_branch`; sorted by `channel`.
""", """
g = loan.groupby('channel')['branch_id']
result = pd.DataFrame({'rows': g.size(), 'with_branch': g.count()})
""", ["loan"]),

    P(3, """
The single largest loan in each `purpose` (ties: smaller `loan_id` wins). Return `purpose`, `loan_id`,
`original_amount`; sorted by `purpose`.
""", """
top = (loan.sort_values(['original_amount', 'loan_id'], ascending=[False, True])
           .groupby('purpose').head(1))
result = top[['purpose', 'loan_id', 'original_amount']].sort_values('purpose')
""", ["loan"], hint="Sort first, then `groupby(...).head(1)` keeps the first row of each group."),

    P(3, """
On `app`, among applications that have a `decision`, the approval rate per `channel` as a percentage
rounded to 2 dp. Return `channel`, `approval_pct`; sorted by `channel`.
""", """
d = app.dropna(subset=['decision'])
result = (100 * (d['decision'] == 'Approved').groupby(d['channel']).mean()).round(2)
""", ["loan_application"]),
])
