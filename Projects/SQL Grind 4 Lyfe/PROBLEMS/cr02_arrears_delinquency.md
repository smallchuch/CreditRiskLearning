# CR02 - Arrears and delinquency reporting

`answers/cr02_arrears_delinquency/qNN.sql` &nbsp;|&nbsp; check with: `grade cr02` or `grade cr02 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: the monthly arrears report

Arrears = loans behind on repayments. The board sees this every month, so you must be exact and reproducible.

```
 DPD (days past due)   0     1-29     30-59    60-89    90-119   120-179   180+
 Common name        Current  Early   Past due  Past due  Default  Default   Default
                              ^ not usually reported      ^ "90+ DPD" = the regulatory default line
```

* **Arrears rate** = arrears loans / all live loans (by count) **or** arrears balance / total balance (by balance). Say which.
* `ref_arrears_bucket` gives the official bucket names (join with `days_past_due BETWEEN dpd_from AND COALESCE(dpd_to, 99999)`).
* `arrears_amount` = dollars behind; `hardship_flag` marks loans under a hardship arrangement (often excluded or reported separately).
* The **live book** = non-closed rows at the reporting snapshot.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Arrears distribution at 2025-12-31: for each official bucket (`ref_arrears_bucket`), loan count and balance (0dp). `bucket_name`, `loans`, `balance`; sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

30+ DPD rate by count and by balance at 2025-12-31 (live book), 2dp %. Return `count_rate_pct`, `balance_rate_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Total dollars in arrears (`SUM(arrears_amount)`, 0dp) on the live book at 2025-12-31, and the number of loans with arrears_amount > 0. Two numbers.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

90+ DPD rate by month-end over 2025 (count basis, 2dp %), live book. `snapshot_date`, `rate_90plus_pct`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

30+ DPD rate (balance basis, 2dp) by `purpose` at 2025-12-31. `purpose`, `rate_pct`; sorted by rate descending, purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

30+ DPD rate (count basis, 2dp) by `channel` at 2025-12-31. `channel`, `rate_pct`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Arrears by repayment type: `repayment_type`, loans, 30+ DPD loans, rate (2dp) at 2025-12-31 live book. Sorted by type.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Excluding hardship: 30+ DPD count at 2025-12-31 split by `hardship_flag` (true/false). `hardship_flag`, `loans_30plus`; sorted by flag.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

LVR band vs arrears: using `ref_lvr_band` on origination LVR (lower exclusive, upper inclusive, first band includes 0), the 30+ DPD rate by band (count basis, 2dp) at 2025-12-31. `band_name`, `loans`, `rate_pct`; sorted by band_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Early-warning list: live loans at 2025-12-31 with `days_past_due` between 1 and 29 that were ALSO in arrears (dpd > 0) the previous month (two consecutive months). Return the count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

State league table of 90+ DPD rate (count basis, 2dp) at 2025-12-31 using property state. Show only states with at least 1,000 live loans. `state`, `live_loans`, `rate_90plus_pct`; sorted by rate descending then state.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Origination-year arrears: for each origination year, 30+ DPD rate (count, 2dp) at 2025-12-31 on live loans. `yr`, `live_loans`, `rate_pct`; sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Months in arrears distribution: for live loans at 2025-12-31 with dpd >= 30 now, how many snapshots (months) in the last 12 (`snapshot_date > 2024-12-31`) had dpd >= 30? Return `months_30plus`, `loans`; sorted by months.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Reconcile arrears dollars to days: loans at 2025-12-31 (live) with `days_past_due >= 30` but `arrears_amount` below one scheduled repayment (`arrears_amount < scheduled_repayment`) - potential data issue. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★ &nbsp; (core)

Arrears at 2019-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

Arrears at 2020-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

Arrears at 2021-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Arrears at 2022-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

Arrears at 2023-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Arrears at 2024-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Arrears at 2025-12-31 (live): 30+ DPD and 90+ DPD rates by count and by balance (2 dp %). `c30`, `c90`, `b30`, `b90`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Property state `'NSW'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Property state `'VIC'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Property state `'QLD'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Property state `'SA'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Property state `'WA'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Property state `'TAS'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Property state `'NT'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Property state `'ACT'` at 2025-12-31: live loans, loans 30+ DPD, 30+ rate (count, 2 dp) and dollars in arrears (0 dp). `loans`, `loans_30plus`, `rate_pct`, `arrears_dollars`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Owner Occupied'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Investment'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Purpose `'Refinance'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Purpose `'Equity Release / Top-up'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Purpose `'Construction'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Purpose `'Internal Refinance'`: the arrears distribution at 2025-12-31 by official bucket (`ref_arrears_bucket`): `bucket_name`, `loans`, `balance` (0 dp); sorted by `bucket_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Channel `'Broker'`: the 30+ DPD rate (count, 2 dp) at each year-end 2022-2025. `snapshot_date`, `rate_pct`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Channel `'Branch'`: the 30+ DPD rate (count, 2 dp) at each year-end 2022-2025. `snapshot_date`, `rate_pct`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Channel `'Digital'`: the 30+ DPD rate (count, 2 dp) at each year-end 2022-2025. `snapshot_date`, `rate_pct`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Channel `'Mobile Lender'`: the 30+ DPD rate (count, 2 dp) at each year-end 2022-2025. `snapshot_date`, `rate_pct`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Hardship effect at 2020-12-31: 30+ DPD loans split by `hardship_flag` (live), with each group's balance (0 dp). `hardship_flag`, `loans`, `balance`; sorted by flag.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Hardship effect at 2022-12-31: 30+ DPD loans split by `hardship_flag` (live), with each group's balance (0 dp). `hardship_flag`, `loans`, `balance`; sorted by flag.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Hardship effect at 2024-12-31: 30+ DPD loans split by `hardship_flag` (live), with each group's balance (0 dp). `hardship_flag`, `loans`, `balance`; sorted by flag.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.
