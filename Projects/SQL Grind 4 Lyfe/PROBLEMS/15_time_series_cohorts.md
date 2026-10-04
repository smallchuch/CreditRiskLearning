# 15 - Time series, cohorts, vintages, point-in-time history

`answers/15_time_series_cohorts/qNN.sql` &nbsp;|&nbsp; check with: `grade 15` or `grade 15 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Time-series patterns every credit analyst uses

**Vintage / cohort analysis** - group loans by when they started, then follow each group as it ages:
```
 vintage (orig. quarter)   MOB 0   MOB 6   MOB 12   MOB 24    <- months on book
 2021-Q1                    0.0%    0.2%    0.6%     1.1%     <- % of loans ever 30+ DPD (cumulative)
 2022-Q1                    0.0%    0.3%    0.9%     --
```
Rows = cohort, columns = age. Lines that fan out upward = deteriorating underwriting.

**Date spine** - a calendar of every period so empty periods still show as 0 (LEFT JOIN onto the spine).

**Point-in-time ("as at") queries** - history tables store changes; "what was true on date X" needs `effective_from <= X AND (effective_to IS NULL OR effective_to > X)`.

**Slowly changing facts** - `loan_rate_history` (rate over time), `property_valuation` (value over time), `application_status_history` (status over time). The *latest* row per key is `ROW_NUMBER() ... = 1` / `QUALIFY`.

**Stock vs flow**: *stock* = a balance at a date (snapshot); *flow* = movement in a period (originations, repayments, write-offs). Balance roll-forward: `opening + originations - repayments - write-offs = closing`.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans originated per quarter, labelled like `2024-Q3`. Return `vintage`, `loans`; sorted by `vintage`. Use `year(...) || '-Q' || quarter(...)`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Total non-closed balance by month-end for the last 6 snapshot dates (2025-07-31 to 2025-12-31). Return `snapshot_date`, `balance` (0dp); sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Number of live (non-closed) loans at each year-end 2019-2025 (snapshot dates 12-31). Return `snapshot_date`, `loans`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Vintage 30+ DPD curve (point values). For loans originated in 2021, the share of loans (1dp %) that are 30+ DPD at months-on-book 12 (`months_on_book = 12`). Return one number, `pct_30plus_mob12` (denominator = loans with a snapshot at MOB 12, non-closed at that date).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

Vintage table by origination year (2019-2024) at MOB 12: `yr`, `loans_at_mob12`, `pct_30plus` (2dp). Non-closed at that point. Sorted by `yr`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Prepayment/attrition by vintage: for origination years 2019-2023, the % of loans closed within 24 months of origination (`closed_date <= origination_date + INTERVAL 24 MONTH`). Return `yr`, `loans`, `closed_24m_pct` (1dp); sorted by `yr`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Point-in-time balance: total balance of the portfolio at 2023-06-30 (snapshot) for non-closed loans, and the number of loans. Two numbers: `loans`, `balance` (0dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★ &nbsp; (core)

Date spine with zeros: for each of the 12 months of 2019 show the number of loans originated (0 if none). Return `month_start`, `loans`; sorted by month. Build the month list with `generate_series` and LEFT JOIN the loans onto it.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Rate in force at a date: for loans 1-20, the interest rate from `loan_rate_history` in force on 2020-06-30 (where it already existed). Return `loan_id`, `interest_rate_pct`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **17 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Latest valuation per property (non-zero, <= 2025-12-31): how many properties have a latest valuation above $1,000,000? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward for Dec 2025 (non-internal loans, all loans): opening balance (snapshot 2025-11-30, non-closed), + new loans originated in Dec (`original_amount`), - closing balance at 2025-12-31 (non-closed). Report `opening`, `originations`, `closing`, and `implied_runoff` = opening + originations - closing (all 0dp). One row.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Cumulative ever-30+ by vintage. For loans originated in 2022, compute at MOB 6, 12, 18, 24 the % of loans that have EVER been 30+ DPD up to that MOB (`MAX(days_past_due)>=30` among snapshots with `months_on_book <= k`). Return `mob`, `loans`, `ever_30plus_pct` (2dp) for k in (6,12,18,24); sorted by `mob`. Loans = those 2022 loans that have a snapshot at that MOB.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Fixed-rate expiry wall. Active loans with fixed expiry dates after the snapshot: balance maturing per quarter. Return `quarter` (label `YYYY-Qn`), `loans`, `balance` (0dp, snapshot 2025-12-31) for fixed expiry dates in 2026; sorted by quarter. Join `loan` and the snapshot.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

IO cliff: Active interest-only loans (snapshot `repayment_type='Interest Only'` at 2025-12-31) with `io_expiry_date` in 2026, by month. Return `io_month` (first day of the month, date), `loans`, `balance` (0dp); sorted by `io_month`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Status history as-at: the status of each application as at 2024-06-30 (last event with `status_ts <= '2024-06-30 23:59:59'`, using the latest event by ts then event_id) for applications lodged between 2024-06-01 and 2024-06-15. Count by `status`. Return `status`, `apps`; sorted by `apps` descending then `status`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Time-to-event: for settled applications, days from 'Submitted' to 'Settled' in `application_status_history` (min `status_ts` per status). Return the median days (1 dp) overall as `median_days`. One number. (Use MIN per application for each status to ignore duplicates.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Seasonality: average loans originated per calendar month number across 2019-2025 (sum of loans by month number / 7 years, 1dp). Return `month_no`, `avg_loans`; sorted by month. (2018 and partial year excluded.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Moving 12-month default flow: for each month-end snapshot in 2025, count loans that are 90+ DPD this month but were NOT 90+ last month (`new_90plus`). Return `snapshot_date`, `new_90plus`; sorted by date. (Non-closed.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Customer tenure vs product: average years between `customer_since` and the customer's first loan origination, per customer `segment` (2dp). Return `segment`, `avg_years`; sorted by segment. (Use `date_diff('day', ...)/365.25`; first loan = MIN origination per primary customer; ignore negatives.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★ &nbsp; (core)

The 2019 vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

The 2020 vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

The 2021 vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

The 2022 vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

The 2023 vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

The 2024 vintage: % of loans (non-closed at that point) that are 30+ DPD at months-on-book 12, and the number of loans observed. `loans`, `pct_30plus` (2 dp).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Attrition: of the loans originated in 2019, the % still open at 24 months on book (has a non-closed snapshot at MOB 24; 1 dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Attrition: of the loans originated in 2020, the % still open at 24 months on book (has a non-closed snapshot at MOB 24; 1 dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Attrition: of the loans originated in 2021, the % still open at 24 months on book (has a non-closed snapshot at MOB 24; 1 dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Attrition: of the loans originated in 2022, the % still open at 24 months on book (has a non-closed snapshot at MOB 24; 1 dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Attrition: of the loans originated in 2023, the % still open at 24 months on book (has a non-closed snapshot at MOB 24; 1 dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★ &nbsp; (warm-up)

Live book at 2019-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★ &nbsp; (warm-up)

Live book at 2020-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★ &nbsp; (warm-up)

Live book at 2021-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★ &nbsp; (warm-up)

Live book at 2022-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★ &nbsp; (warm-up)

Live book at 2023-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★ &nbsp; (warm-up)

Live book at 2024-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★ &nbsp; (warm-up)

Live book at 2025-12-31: number of non-closed loans and total balance (0 dp). `loans`, `balance`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward for December 2021: opening balance (live, 2021-11-30), new loans originated in December 2021, closing balance (live, 2021-12-31) and implied run-off = opening + new - closing (0 dp). `opening`, `new_lending`, `closing`, `implied_runoff`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward for December 2022: opening balance (live, 2022-11-30), new loans originated in December 2022, closing balance (live, 2022-12-31) and implied run-off = opening + new - closing (0 dp). `opening`, `new_lending`, `closing`, `implied_runoff`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward for December 2023: opening balance (live, 2023-11-30), new loans originated in December 2023, closing balance (live, 2023-12-31) and implied run-off = opening + new - closing (0 dp). `opening`, `new_lending`, `closing`, `implied_runoff`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward for December 2024: opening balance (live, 2024-11-30), new loans originated in December 2024, closing balance (live, 2024-12-31) and implied run-off = opening + new - closing (0 dp). `opening`, `new_lending`, `closing`, `implied_runoff`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Balance roll-forward for December 2025: opening balance (live, 2025-11-30), new loans originated in December 2025, closing balance (live, 2025-12-31) and implied run-off = opening + new - closing (0 dp). `opening`, `new_lending`, `closing`, `implied_runoff`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Vintage curve for `'Purchase - Owner Occupied'` loans originated in 2022: the 30+ DPD rate (2 dp, non-closed) at MOB 6, 12, 18 and 24 as four columns. `mob6`, `mob12`, `mob18`, `mob24`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★★ &nbsp; (challenge)

Vintage curve for `'Purchase - Investment'` loans originated in 2022: the 30+ DPD rate (2 dp, non-closed) at MOB 6, 12, 18 and 24 as four columns. `mob6`, `mob12`, `mob18`, `mob24`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★★ &nbsp; (challenge)

Vintage curve for `'Refinance'` loans originated in 2022: the 30+ DPD rate (2 dp, non-closed) at MOB 6, 12, 18 and 24 as four columns. `mob6`, `mob12`, `mob18`, `mob24`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q46 &nbsp; ★★★ &nbsp; (challenge)

Vintage curve for `'Equity Release / Top-up'` loans originated in 2022: the 30+ DPD rate (2 dp, non-closed) at MOB 6, 12, 18 and 24 as four columns. `mob6`, `mob12`, `mob18`, `mob24`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q47 &nbsp; ★★★ &nbsp; (challenge)

Vintage curve for `'Construction'` loans originated in 2022: the 30+ DPD rate (2 dp, non-closed) at MOB 6, 12, 18 and 24 as four columns. `mob6`, `mob12`, `mob18`, `mob24`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
