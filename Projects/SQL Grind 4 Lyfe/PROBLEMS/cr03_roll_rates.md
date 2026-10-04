# CR03 - Roll rates, cures and transitions

`answers/cr03_roll_rates/qNN.sql` &nbsp;|&nbsp; check with: `grade cr03` or `grade cr03 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: roll rates - the engine of loss forecasting

A **roll-rate matrix** shows where loans in one arrears bucket are a month later.

```
                 NEXT MONTH
 THIS MONTH     Current  1-29   30-59  60-89  90+
 Current          97%     3%     0      0      0
 1-29             40%    35%    25%     0      0       <- 40% cure, 25% roll worse
 30-59            10%     5%    30%    55%     0
```

Build it with `LAG`/`LEAD`: pair each loan-month with the next month for the same loan, bucket both, count pairs.

```
 WITH m AS (SELECT loan_id, snapshot_date, bucket(dpd) AS b,
                   LEAD(bucket(dpd)) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS b_next
            FROM loan_monthly_snapshot WHERE loan_status <> 'Closed')
 SELECT b, b_next, COUNT(*) FROM m WHERE b_next IS NOT NULL GROUP BY 1,2
```
Rows should sum to 100% - divide each count by its row total with a window: `COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY b)`.

Buckets used here: `0` Current, `1` (1-29), `2` (30-59), `3` (60-89), `4` (90+).
Caveat: months where a loan closes don't have a "next" - they drop out. Missing snapshots (a planted data quirk) can fake a "next month".

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

How many loan-month transitions exist for non-closed loans in 2025 (a loan with a next-month snapshot)? Use LEAD on `snapshot_date` per loan across all history; count rows where `snapshot_date` is in 2025 and a next row exists and the loan is non-closed this month. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Bucket counts at 2025-11-30 (live): bucket 0-4 using: 0 = current, 1 = 1-29, 2 = 30-59, 3 = 60-89, 4 = 90+. Return `bucket`, `loans`; sorted by bucket.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★★ &nbsp; (core)

Transition matrix counts for Nov-30-2025 -> Dec-31-2025 (non-closed in Nov, with a Dec row): `from_bucket`, `to_bucket`, `loans` using the 0-4 buckets. Sorted by from, to.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **14 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Roll rate from Current: for the 2025-11-30 -> 2025-12-31 transition, % of Current loans (bucket 0) that moved to 1-29 or worse (2dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

Cure rate: of loans in bucket 1 (1-29 DPD) at 2025-11-30 with a Dec row, the % at 0 DPD by 2025-12-31 (1dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★★ &nbsp; (challenge)

Full 12-month pooled roll matrix: pool all month-pairs from 2025-01-31 to 2025-12-31 (current month in Jan..Nov 2025 with the next row = the consecutive month-end). Return `from_bucket`, `to_bucket`, `loans`, `row_pct` (1dp, share of the from-bucket); sorted by from, to. Pairs only where next month's snapshot date is the next month-end.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **16 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★★ &nbsp; (challenge)

Worsening vs improving: for the pooled 2025 pairs above, the share of loan-months (all buckets) where the bucket got worse, stayed, or improved. Return `worse_pct`, `same_pct`, `better_pct` (2dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Time to cure: for loans that entered 30+ DPD in 2024 for the first time in that year (first month in 2024 with dpd >= 30 and dpd < 30 the month before), how many returned to 0 DPD within 6 months? Return `entered`, `cured_within_6m`, `cure_rate_pct` (1dp). Use snapshot months_on_book as the clock (`months_on_book` + 1 to + 6).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

Default flow: loans whose first-ever 90+ DPD month is in each quarter of 2024 and 2025. `quarter` (label `YYYY-Qn`), `new_defaults`; sorted by quarter. Non-closed rows only for the 90+ test.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Re-default: loans that were 90+ DPD, later reached 0 DPD (cured), then went 30+ again. Count such loans. One number. Hint: self-join snapshots by loan and ordered months (e.g. three `EXISTS` with increasing `months_on_book`).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-01-31 (live, with a row on 2025-02-28), the % that were behind (1+ DPD) on 2025-02-28 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-02-28 (live, with a row on 2025-03-31), the % that were behind (1+ DPD) on 2025-03-31 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-03-31 (live, with a row on 2025-04-30), the % that were behind (1+ DPD) on 2025-04-30 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-04-30 (live, with a row on 2025-05-31), the % that were behind (1+ DPD) on 2025-05-31 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-05-31 (live, with a row on 2025-06-30), the % that were behind (1+ DPD) on 2025-06-30 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-06-30 (live, with a row on 2025-07-31), the % that were behind (1+ DPD) on 2025-07-31 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-07-31 (live, with a row on 2025-08-31), the % that were behind (1+ DPD) on 2025-08-31 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-08-31 (live, with a row on 2025-09-30), the % that were behind (1+ DPD) on 2025-09-30 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-09-30 (live, with a row on 2025-10-31), the % that were behind (1+ DPD) on 2025-10-31 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-10-31 (live, with a row on 2025-11-30), the % that were behind (1+ DPD) on 2025-11-30 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Roll from Current: of loans at 0 DPD on 2025-11-30 (live, with a row on 2025-12-31), the % that were behind (1+ DPD) on 2025-12-31 (3 dp %). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-01-31 with a row on 2025-02-28, the % at 0 DPD on 2025-02-28 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-02-28 with a row on 2025-03-31, the % at 0 DPD on 2025-03-31 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-03-31 with a row on 2025-04-30, the % at 0 DPD on 2025-04-30 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-04-30 with a row on 2025-05-31, the % at 0 DPD on 2025-05-31 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-05-31 with a row on 2025-06-30, the % at 0 DPD on 2025-06-30 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-06-30 with a row on 2025-07-31, the % at 0 DPD on 2025-07-31 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-07-31 with a row on 2025-08-31, the % at 0 DPD on 2025-08-31 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-08-31 with a row on 2025-09-30, the % at 0 DPD on 2025-09-30 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-09-30 with a row on 2025-10-31, the % at 0 DPD on 2025-10-31 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-10-31 with a row on 2025-11-30, the % at 0 DPD on 2025-11-30 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★★ &nbsp; (challenge)

Cure rate: of live loans at 1-29 DPD on 2025-11-30 with a row on 2025-12-31, the % at 0 DPD on 2025-12-31 (1 dp %), and the number observed. `observed`, `cure_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Purchase - Owner Occupied'`: transition counts 2025-11-30 -> 2025-12-31 as `from_bucket`, `to_bucket`, `loans` (buckets 0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+; live loans with a December row). Sorted by from, to.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **14 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Purchase - Investment'`: transition counts 2025-11-30 -> 2025-12-31 as `from_bucket`, `to_bucket`, `loans` (buckets 0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+; live loans with a December row). Sorted by from, to.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **14 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Refinance'`: transition counts 2025-11-30 -> 2025-12-31 as `from_bucket`, `to_bucket`, `loans` (buckets 0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+; live loans with a December row). Sorted by from, to.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **14 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Equity Release / Top-up'`: transition counts 2025-11-30 -> 2025-12-31 as `from_bucket`, `to_bucket`, `loans` (buckets 0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+; live loans with a December row). Sorted by from, to.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Construction'`: transition counts 2025-11-30 -> 2025-12-31 as `from_bucket`, `to_bucket`, `loans` (buckets 0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+; live loans with a December row). Sorted by from, to.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.
