# cr01 - Portfolio composition and concentration

`answers/cr01_portfolio/qNN.py` &nbsp;|&nbsp; check with: `grade cr01` or `grade cr01 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** (a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Live book at 2025-12-31: number of loans and total balance in **$ millions** (2 dp). Return one row:
`loans`, `balance_m`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q02 &nbsp; ★ &nbsp; (warm-up)

Live balance share by `purpose` (join from `loan`), as a percentage rounded to 2 dp. Return `purpose`, `balance_pct`;
sorted by `balance_pct` (largest first).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q03 &nbsp; ★★ &nbsp; (core)

Balance-weighted average **origination** LVR of the live book, by `channel` (weights = current `closing_balance`),
rounded to 2 dp. Return `channel`, `wavg_lvr`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q04 &nbsp; ★★ &nbsp; (core)

Top-1% concentration: what percentage of live balance sits in the largest 1% of live loans by balance
(the top `ceil(1% of loan count)` loans)? Round to 2 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`

### Q05 &nbsp; ★★ &nbsp; (core)

Live balance by **origination LVR band** (`ref_lvr_band` edges, left-closed: `<= 60%`, `60-70%`, `70-80%`, `80-90%`,
`90-95%`, `> 95%`). Return `band`, `balance_m` (2 dp), `balance_pct` (2 dp) in band order.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`

### Q06 &nbsp; ★★ &nbsp; (core)

Live balance in $ millions (1 dp) by `occupancy` (rows, from `dim_product` via `loan`) and the snapshot's
`repayment_type` (columns). Return `occupancy`, `Interest Only`, `P&I`; sorted by `occupancy`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described. &nbsp;|&nbsp; tables: `snap`, `loan`, `dim_product`

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Broker concentration: among live loans written by a broker (`broker_id` not missing), the **HHI** of balance across
brokers = sum over brokers of (balance share in %)^2. Round to 1 dp.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter. &nbsp;|&nbsp; tables: `snap`, `loan`
