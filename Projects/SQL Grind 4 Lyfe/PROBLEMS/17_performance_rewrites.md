# 17 - Rewrite for clarity and speed

`answers/17_performance_rewrites/qNN.sql` &nbsp;|&nbsp; check with: `grade 17` or `grade 17 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Writing SQL that doesn't take all afternoon

You don't need to be a DBA, but you should know *why* a query is slow:

```
 Slow patterns                              Faster rewrite
 ------------------------------------------ ----------------------------------------------------
 SELECT * on a wide table                    select only the columns you need
 function on a filtered column               year(d) = 2024   ->   d >= '2024-01-01' AND d < '2025-01-01'
 correlated subquery per row                 join to a pre-aggregated table, or a window function
 DISTINCT to hide a join fan-out             fix the join grain (aggregate first / EXISTS)
 NOT IN (subquery)                           NOT EXISTS
 UNION (needless dedupe)                     UNION ALL
 filter AFTER a huge join                    filter / aggregate BEFORE joining (CTE)
 COUNT(DISTINCT) everywhere                  fine in DuckDB, but check the grain first
```

Use `EXPLAIN` / `EXPLAIN ANALYZE` in the DuckDB shell to see the plan: look for big joins on the wrong side and full scans.
In this sandbox the checker only compares RESULTS - but each task says what the "naive" approach is so you practise the better one. Keep a note of why yours is better.

Habit: read from the smallest table / filter earliest / aggregate before joining.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(origination_date) = 2024`. Rewrite as a range filter and return the count of 2024 loans. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Naive: `SELECT *` then look at one thing. Return only `loan_id`, `original_amount` for the 5 biggest loans (largest first, tie `loan_id`).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Naive: `UNION` of two disjoint sets. Combine loans with `purpose='Construction'` and `purpose='Refinance'` loan counts using `UNION ALL`. Return `purpose`, `loans`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Naive: a correlated subquery computing each customer's loan count. Rewrite with a pre-aggregated join: number of customers with exactly 2 loans as primary. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★★ &nbsp; (core)

Naive: `DISTINCT` after joining `loan` to `loan_borrower` to count loans with a co-borrower. Rewrite using `EXISTS` (or a semi-join). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Naive: `NOT IN (SELECT loan_id FROM hardship_arrangement)`. Rewrite with `NOT EXISTS` and count loans never in hardship. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

Naive: join all 2 million snapshot rows to `loan` before filtering. Filter the snapshot to 2025-12-31 FIRST (CTE), then join, and return total balance by `purpose`. `purpose`, `balance` (0dp); sorted by purpose. (Non-closed only.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Naive: three separate queries for approved, declined and withdrawn counts. Do it in ONE pass with conditional aggregation. Return one row: `approved` (`decision = 'Approved'`), `declined` (`decision = 'Declined'`), `withdrawn` (`current_status = 'Withdrawn'`).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★ &nbsp; (core)

Naive: self-join to get each customer's latest application. Rewrite with `QUALIFY ROW_NUMBER()`. Return the count of customers whose latest application (by date, then id) was Declined. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

Naive: `SELECT COUNT(DISTINCT customer_id)` via a big join. Count distinct customers who have ever been 90+ DPD with a semi-join: customers (`primary_customer_id`) having a loan with `EXISTS` a snapshot dpd>=90. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Naive: 12 near-identical queries for monthly originations in 2025. Do it with one GROUP BY. Return `month_no`, `loans`, `amount` (0dp); sorted by month.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Naive: correlated `MAX` subquery to get each loan's latest snapshot. Rewrite with `QUALIFY` or `arg_max`: total closing balance of every loan's LAST snapshot row for loans with `loan_id <= 100`. One number (0dp).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Naive: functions on both sides of a join (`LOWER(a.x)=LOWER(b.x)`) are slow. Count customers that share an email with another customer using GROUP BY on `LOWER(email)` rather than a self-join. One number: customers whose lowercase email is shared.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Naive: window over everything then filter. Compute the top 3 largest loans per state of the property efficiently: first reduce to only the columns needed, then rank. Return `state`, `loan_id`, `original_amount`; sorted by state, amount descending, loan_id. Top 3 per state.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Naive: count how many loans had a 30+ DPD month by scanning with `IN (SELECT ...)`. Rewrite as an aggregate over the snapshot then count. One number: loans with `MAX(days_past_due) >= 30`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Naive: join `loan_payment` (900k rows) to everything. Aggregate payments first: per `payment_status`, count and total (0dp) of payments made in the last 3 months to 2025-12-31 (`payment_date > 2025-09-30`). `payment_status`, `n`, `total`; sorted by status.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2019`. Rewrite as a half-open date range and return the number of applications in 2019. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2020`. Rewrite as a half-open date range and return the number of applications in 2020. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2021`. Rewrite as a half-open date range and return the number of applications in 2021. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2022`. Rewrite as a half-open date range and return the number of applications in 2022. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2023`. Rewrite as a half-open date range and return the number of applications in 2023. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2024`. Rewrite as a half-open date range and return the number of applications in 2024. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★ &nbsp; (warm-up)

Naive: `WHERE year(application_date) = 2025`. Rewrite as a half-open date range and return the number of applications in 2025. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Naive: `SELECT DISTINCT` after joining `loan` to `loan_borrower`. Rewrite with EXISTS: how many `'Purchase - Owner Occupied'` loans have a co-applicant? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Naive: `SELECT DISTINCT` after joining `loan` to `loan_borrower`. Rewrite with EXISTS: how many `'Purchase - Investment'` loans have a co-applicant? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Naive: `SELECT DISTINCT` after joining `loan` to `loan_borrower`. Rewrite with EXISTS: how many `'Refinance'` loans have a co-applicant? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Naive: `SELECT DISTINCT` after joining `loan` to `loan_borrower`. Rewrite with EXISTS: how many `'Equity Release / Top-up'` loans have a co-applicant? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Naive: `SELECT DISTINCT` after joining `loan` to `loan_borrower`. Rewrite with EXISTS: how many `'Construction'` loans have a co-applicant? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Naive: correlated subquery per row to get each customer's loan count. Rewrite with a pre-aggregation: customers with 3 or more loans via `'Broker'`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Naive: correlated subquery per row to get each customer's loan count. Rewrite with a pre-aggregation: customers with 3 or more loans via `'Branch'`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

Naive: correlated subquery per row to get each customer's loan count. Rewrite with a pre-aggregation: customers with 3 or more loans via `'Digital'`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

Naive: correlated subquery per row to get each customer's loan count. Rewrite with a pre-aggregation: customers with 3 or more loans via `'Mobile Lender'`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★ &nbsp; (core)

Naive: join all snapshot rows then filter. Filter the snapshot to 2021-12-31 first, then join: live balance (0 dp) by `channel`. `channel`, `balance`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Naive: join all snapshot rows then filter. Filter the snapshot to 2023-12-31 first, then join: live balance (0 dp) by `channel`. `channel`, `balance`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Naive: join all snapshot rows then filter. Filter the snapshot to 2025-12-31 first, then join: live balance (0 dp) by `channel`. `channel`, `balance`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Naive: self-join for the latest status event. Use `QUALIFY ROW_NUMBER()` to get each application's latest event (by ts, then event_id) and count how many of the latest events are `'Settled'`... for applications 1 to 3000. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Naive: self-join for the latest status event. Use `QUALIFY ROW_NUMBER()` to get each application's latest event (by ts, then event_id) and count how many of the latest events are `'Settled'`... for applications 1 to 5000. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Naive: self-join for the latest status event. Use `QUALIFY ROW_NUMBER()` to get each application's latest event (by ts, then event_id) and count how many of the latest events are `'Settled'`... for applications 1 to 10000. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
