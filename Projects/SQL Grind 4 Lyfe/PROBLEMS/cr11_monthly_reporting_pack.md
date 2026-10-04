# CR11 - Building the monthly reporting pack

`answers/cr11_monthly_reporting_pack/qNN.sql` &nbsp;|&nbsp; check with: `grade cr11` or `grade cr11 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: build the monthly credit risk pack

Every month the head of credit risk gets one pack. You assemble it with SQL. Think **KPI table**: one row per month, one column per KPI - the shape that feeds Power BI / Excel charts.

```
 month_end | live_loans | balance | new_loans | new_balance | 30+ rate | 90+ rate | closed | net growth
```
Patterns used: month-end spine, conditional aggregation, `LAG` for movement, balance roll-forward (opening + new - repayments/closures = closing), YTD with a window (`SUM() OVER (PARTITION BY year ORDER BY month)`).
Always state the definition of every KPI in a comment - the real job is making numbers that are *the same every time*.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Live loans and total balance at each month-end of 2025. `snapshot_date`, `loans`, `balance` (0dp); sorted by date.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

New lending by month 2025: loans and $ (0dp). `month_start`, `new_loans`, `new_amount`; sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Loans closed by month in 2025 by count (use `closed_date`). `month_start`, `closed_loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

One KPI table, 2025 month-ends: `snapshot_date`, `live_loans`, `balance` (0dp), `pct_30plus` (count, 2dp), `pct_90plus` (count, 2dp). Sorted by date.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Net loan growth: for each 2025 month, `new_loans` minus `closed_loans` and the change in live loan count (from snapshots). Return `month_start`, `new_loans`, `closed_loans`, `net_flow`, `live_change` for Feb-Dec 2025; sorted by month. (live_change = live now - live last month-end.)

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Year-to-date new lending: monthly new amount and YTD cumulative (0dp) for 2024 and 2025 using `SUM() OVER (PARTITION BY year ORDER BY month)`. `yr`, `mon`, `new_amount`, `ytd_amount`; sorted by year, month.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward by month for 2025 (Feb-Dec): `opening` (prior month-end live balance), `new_lending` (loans originated in the month), `closing` (live balance), and `other_movements` = closing - opening - new_lending (repayments, closures, interest; 0dp). `month_end`, `opening`, `new_lending`, `closing`, `other_movements`; sorted by date.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Top movers: the 5 `purpose` x `channel` segments whose live balance grew most between 2024-12-31 and 2025-12-31 (absolute $, 0dp). `purpose`, `channel`, `growth`; sorted by growth descending.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

A one-row 'executive summary' for 2025-12-31: live loans, balance ($m, 1dp), % 90+ DPD (2dp), total ECL ($m, 1dp), ECL coverage (2dp %), new lending in Q4 2025 ($m, 1dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `q4_new_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Rolling 12-month new lending: for each month-end from Dec 2019 to Dec 2025, the sum of new lending in the latest 12 months ($m, 1dp). Use a window `ROWS BETWEEN 11 PRECEDING AND CURRENT ROW` over a monthly series. Return only the December rows: `month_start`, `rolling_12m_m`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Branch scorecard for 2025: for each branch with at least 60 loans originated in 2025: loans, $ (0dp), average LVR (1dp). Top 5 by $ . `branch_name`, `loans`, `amount`, `avg_lvr`; sorted by amount descending.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-01-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-02-28: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-03-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-04-30: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-05-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-06-30: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-07-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-08-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-09-30: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-10-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-11-30: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

KPI row for the month ending 2025-12-31: live loans, balance (0 dp), 30+ DPD rate (count, 2 dp %), 90+ DPD rate (count, 2 dp %), new loans originated in that month, new lending (0 dp). `live_loans`, `balance`, `pct_30plus`, `pct_90plus`, `new_loans`, `new_amount`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2019-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2019 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2020-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2020 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2021-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2021 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2022-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2022 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2023-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2023 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2024-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2024 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

Executive summary for 2025-12-31: live loans, balance in $m (1 dp), 90+ DPD rate (2 dp %), ECL in $m (1 dp), coverage (2 dp %), new lending in 2025 in $m (1 dp). `live_loans`, `balance_m`, `pct_90plus`, `ecl_m`, `coverage_pct`, `new_lending_m`.

> Return **6 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
