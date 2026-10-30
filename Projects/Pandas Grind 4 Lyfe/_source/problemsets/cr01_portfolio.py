from . import P

PRIMER = r"""
**Credit-risk scenario.** Things you'd be asked for in a monthly portfolio pack. Every pattern here is from sets 03 to 09.

## The live book
```python
asat = '2025-12-31'
live = snap[(snap['snapshot_date'] == asat) & (snap['loan_status'] != 'Closed')]
```
`snap` keeps the closing month (balance 0, status `'Closed'`), so always drop it.

## Count share vs balance share
```
 segment   loans  balance     count share   balance share
 A         900    $180m       90%           60%
 B         100    $120m       10%           40%    <- B is 10% of loans but 40% of the money
```
Concentration questions are almost always about **balance**.

## Concentration measures

| Measure | Formula |
|---|---|
| Top-N share | balance of the N largest / total |
| HHI | sum of (share as %)^2 across groups: 10,000 = one group has everything, near 0 = spread out |
| Weighted average | `(x * bal).sum() / bal.sum()` |
"""

LIVE = "live = snap[(snap['snapshot_date'] == '2025-12-31') & (snap['loan_status'] != 'Closed')]\n"

CONCEPT = dict(id="cr01_portfolio", title="cr01 - Portfolio composition and concentration", primer=PRIMER, problems=[
    P(1, """
Live book at 2025-12-31: number of loans and total balance in **$ millions** (2 dp). Return one row:
`loans`, `balance_m`.
""", LIVE + """
result = pd.DataFrame({'loans': [len(live)], 'balance_m': [round(live['closing_balance'].sum() / 1e6, 2)]})
""", ["loan_monthly_snapshot"]),

    P(1, """
Live balance share by `purpose` (join from `loan`), as a percentage rounded to 2 dp. Return `purpose`, `balance_pct`;
sorted by `balance_pct` (largest first).
""", LIVE + """
m = live[['loan_id', 'closing_balance']].merge(loan[['loan_id', 'purpose']], on='loan_id')
share = 100 * m.groupby('purpose')['closing_balance'].sum() / m['closing_balance'].sum()
result = share.round(2).sort_values(ascending=False)
""", ["loan_monthly_snapshot", "loan"]),

    P(2, """
Balance-weighted average **origination** LVR of the live book, by `channel` (weights = current `closing_balance`),
rounded to 2 dp. Return `channel`, `wavg_lvr`; sorted by `channel`.
""", LIVE + """
m = live[['loan_id', 'closing_balance']].merge(loan[['loan_id', 'channel', 'lvr_at_origination_pct']], on='loan_id')
m['w'] = m['lvr_at_origination_pct'] * m['closing_balance']
g = m.groupby('channel')[['w', 'closing_balance']].sum()
result = (g['w'] / g['closing_balance']).round(2)
""", ["loan_monthly_snapshot", "loan"]),

    P(2, """
Top-1% concentration: what percentage of live balance sits in the largest 1% of live loans by balance
(the top `ceil(1% of loan count)` loans)? Round to 2 dp.
""", LIVE + """
import math
n = math.ceil(0.01 * len(live))
result = round(100 * live['closing_balance'].nlargest(n).sum() / live['closing_balance'].sum(), 2)
""", ["loan_monthly_snapshot"]),

    P(2, """
Live balance by **origination LVR band** (`ref_lvr_band` edges, left-closed: `<= 60%`, `60-70%`, `70-80%`, `80-90%`,
`90-95%`, `> 95%`). Return `band`, `balance_m` (2 dp), `balance_pct` (2 dp) in band order.
""", LIVE + """
m = live[['loan_id', 'closing_balance']].merge(loan[['loan_id', 'lvr_at_origination_pct']], on='loan_id')
labels = ['<= 60%', '60-70%', '70-80%', '80-90%', '90-95%', '> 95%']
m['band'] = pd.cut(m['lvr_at_origination_pct'], [0, 60, 70, 80, 90, 95, np.inf], right=False, labels=labels)
bal = m.groupby('band', observed=False)['closing_balance'].sum()
result = pd.DataFrame({'balance_m': (bal / 1e6).round(2), 'balance_pct': (100 * bal / bal.sum()).round(2)})
""", ["loan_monthly_snapshot", "loan"], order=True),

    P(2, """
Live balance in $ millions (1 dp) by `occupancy` (rows, from `dim_product` via `loan`) and the snapshot's
`repayment_type` (columns). Return `occupancy`, `Interest Only`, `P&I`; sorted by `occupancy`.
""", LIVE + """
m = (live[['loan_id', 'closing_balance', 'repayment_type']]
     .merge(loan[['loan_id', 'product_id']], on='loan_id')
     .merge(dim_product[['product_id', 'occupancy']], on='product_id'))
result = (m.pivot_table(index='occupancy', columns='repayment_type', values='closing_balance', aggfunc='sum') / 1e6).round(1)
""", ["loan_monthly_snapshot", "loan", "dim_product"]),

    P(3, """
Broker concentration: among live loans written by a broker (`broker_id` not missing), the **HHI** of balance across
brokers = sum over brokers of (balance share in %)^2. Round to 1 dp.
""", LIVE + """
m = live[['loan_id', 'closing_balance']].merge(loan[['loan_id', 'broker_id']], on='loan_id').dropna(subset=['broker_id'])
share = 100 * m.groupby('broker_id')['closing_balance'].sum() / m['closing_balance'].sum()
result = round((share ** 2).sum(), 1)
""", ["loan_monthly_snapshot", "loan"]),
])
