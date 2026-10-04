# CR06 - Pricing, rate changes and payment shock

`answers/cr06_pricing_rate_shock/qNN.sql` &nbsp;|&nbsp; check with: `grade cr06` or `grade cr06 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: the RBA moved rates - who is exposed?

Variable loans reprice with the RBA cash rate (with a ~10-day bank lag, see `ref_rba_cash_rate.bank_effective_date`). Fixed loans are protected until `fixed_rate_expiry_date`, then **revert** (the "fixed-rate cliff"). Interest-only loans face a **payment shock** when `io_expiry_date` passes and they convert to P&I.

```
 monthly repayment (P&I):   M = P * r / (1 - (1+r)^-n)        r = annual rate / 12, n = months remaining
 +1% on a $600k, 25-year loan at 6%:  $3,866  ->  $4,228   (+9.4%)   <- the stress test lenders run
```

Your toolkit:
* Snapshot balance + rate give the current exposure.
* `loan_rate_history` gives the rate path of each loan (effective_from/to).
* `loan_event` records reversions ('Fixed rate expired - reverted to variable'), IO conversions and retention discounts.
* Repayment shock = new repayment / old repayment - 1.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

RBA cash-rate decisions: number of increases and decreases (by `change_bps`) in `ref_rba_cash_rate`. Return `hikes`, `cuts` (ignore the starting row with NULL change).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Average origination rate (3dp) per origination year for variable loans only. `yr`, `avg_rate`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

How many 'Fixed rate expired - reverted to variable' events happened in each calendar year? `yr`, `events`; sorted by year.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Pass-through lag: for each RBA decision the `bank_effective_date - decision_date` in days. Return the distinct lag values and count of decisions. `lag_days`, `decisions`; sorted by lag.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Retention discounts: loans that received a 'Retention discount' rate change - count, and average discount in percentage points (the rate change at that effective date versus the prior row's rate; 2dp). Use LAG on `loan_rate_history` per loan. `loans_discounted`, `avg_cut_pp`. One row (cut positive).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Fixed-rate cliff 2026: live loans (snapshot 2025-12-31) with fixed expiry in 2026: count, balance (0dp) and balance-weighted current rate (3dp). `loans`, `balance`, `wtd_rate`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

Average variable rate on the live book at each of the last 4 year-ends 2022-2025 (balance-weighted, 3dp), rate_type Variable loans (use `loan.rate_type`) and non-closed. `snapshot_date`, `wtd_rate`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Stress test: for live P&I loans at 2025-12-31 compute each loan's current repayment from balance, current rate and remaining term (`term_months - months_on_book`, floor 1), and the repayment at +3pp. Report the total monthly repayment now and stressed (0dp) and % increase (1dp) for loans with remaining term >= 12. `now_total`, `stress_total`, `increase_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

IO conversion shock: loans that converted IO -> P&I in 2025 (event 'Interest-only period ended - converted to P&I' in 2025). Average scheduled repayment the month BEFORE and the month AFTER the event month, using the snapshots (the event month's `snapshot_date` = last_day(event_date)). `loans`, `avg_before`, `avg_after`, `increase_pct` (all 1dp except loans). Pairs where both snapshots exist.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Customers who got a retention discount and later closed with 'Refinanced to another lender' anyway: count. One number. (Join `loan_event` 'Retention discount applied' to loan closure reason.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Spread to cash rate: for the live variable book at 2025-12-31, the balance-weighted average margin over the latest RBA cash rate (`cash_rate_pct` of the row with the latest `bank_effective_date <= 2025-12-31`), 2dp. One number: `wtd_margin_pp`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Delinquency after a hike: 30+ DPD rate (count, 2dp) at each month-end of 2023 (snapshot dates in 2023) for live loans. `snapshot_date`, `rate_pct`; sorted by date. (Compare it with the hiking cycle in `ref_rba_cash_rate`.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2019: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2020: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2021: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2022: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2023: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2024: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★ &nbsp; (warm-up)

Origination pricing in 2025: average origination rate (3 dp) for `'Fixed'` and `'Variable'` loans. `avg_fixed`, `avg_variable`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Fixed-rate cliff, 2026 Q1: live loans (2025-12-31) whose fixed term expires in the quarter - loans, balance (0 dp), balance-weighted current rate (3 dp). `loans`, `balance`, `wtd_rate`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Fixed-rate cliff, 2026 Q2: live loans (2025-12-31) whose fixed term expires in the quarter - loans, balance (0 dp), balance-weighted current rate (3 dp). `loans`, `balance`, `wtd_rate`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Fixed-rate cliff, 2026 Q3: live loans (2025-12-31) whose fixed term expires in the quarter - loans, balance (0 dp), balance-weighted current rate (3 dp). `loans`, `balance`, `wtd_rate`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Fixed-rate cliff, 2026 Q4: live loans (2025-12-31) whose fixed term expires in the quarter - loans, balance (0 dp), balance-weighted current rate (3 dp). `loans`, `balance`, `wtd_rate`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★★ &nbsp; (challenge)

Stress test +1pp: for live P&I loans at 2025-12-31 with at least 12 months of term left, total monthly repayment now and at +1 percentage points (0 dp) and % increase (1 dp). Remaining term = `term_months - months_on_book`. `now_total`, `stress_total`, `increase_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★★ &nbsp; (challenge)

Stress test +2pp: for live P&I loans at 2025-12-31 with at least 12 months of term left, total monthly repayment now and at +2 percentage points (0 dp) and % increase (1 dp). Remaining term = `term_months - months_on_book`. `now_total`, `stress_total`, `increase_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

Stress test +3pp: for live P&I loans at 2025-12-31 with at least 12 months of term left, total monthly repayment now and at +3 percentage points (0 dp) and % increase (1 dp). Remaining term = `term_months - months_on_book`. `now_total`, `stress_total`, `increase_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Events in 2022: counts of each `loan_event` type (`event_type`, `events`); sorted by events descending then type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

Events in 2023: counts of each `loan_event` type (`event_type`, `events`); sorted by events descending then type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★ &nbsp; (core)

Events in 2024: counts of each `loan_event` type (`event_type`, `events`); sorted by events descending then type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

Events in 2025: counts of each `loan_event` type (`event_type`, `events`); sorted by events descending then type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Owner Occupied'`: weighted average rate (3 dp) of the live book at each year-end 2022-2025. `snapshot_date`, `wtd_rate`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Investment'`: weighted average rate (3 dp) of the live book at each year-end 2022-2025. `snapshot_date`, `wtd_rate`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Purpose `'Refinance'`: weighted average rate (3 dp) of the live book at each year-end 2022-2025. `snapshot_date`, `wtd_rate`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Purpose `'Equity Release / Top-up'`: weighted average rate (3 dp) of the live book at each year-end 2022-2025. `snapshot_date`, `wtd_rate`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Purpose `'Construction'`: weighted average rate (3 dp) of the live book at each year-end 2022-2025. `snapshot_date`, `wtd_rate`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.
