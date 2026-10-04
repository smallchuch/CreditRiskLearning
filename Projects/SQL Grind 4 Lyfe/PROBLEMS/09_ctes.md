# 09 - CTEs and recursive queries

`answers/09_ctes/qNN.sql` &nbsp;|&nbsp; check with: `grade 09` or `grade 09 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## CTE = a named step. Write the query as a story, top to bottom.

```
 WITH step1 AS ( ... ),          -- 'first, get X'
      step2 AS ( ... FROM step1 ), -- 'then, using X, get Y'
 SELECT ... FROM step2;          -- 'finally, show Y'
```

Why: readable, reusable twice in the same query, easy to debug (run each step alone).

```
 loans -> [monthly_totals] -> [with_prior_month] -> final answer
```

**Recursive CTE** - a query that calls itself, used for hierarchies and sequences:
```
 WITH RECURSIVE chain AS (
     SELECT staff_id, manager_staff_id, 1 AS depth FROM dim_staff WHERE manager_staff_id IS NULL   -- anchor
     UNION ALL
     SELECT s.staff_id, s.manager_staff_id, c.depth+1
     FROM dim_staff s JOIN chain c ON s.manager_staff_id = c.staff_id                               -- recursive step
 )
 SELECT * FROM chain;
```
Anchor = the starting rows; recursive part = "find the next level"; stops when no new rows.
You can also generate a date spine: `SELECT unnest(generate_series(DATE '2025-01-01', DATE '2025-12-31', INTERVAL 1 DAY))`.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Using a CTE named `big` of loans over $1,000,000, count them by `purpose`. Return `purpose`, `loans`; sorted by `loans` descending then `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

CTE of yearly loan counts, then select years with more than 9,000 loans. Return `yr`, `loans`; sorted by `yr`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Two CTEs: `a` = count of loans, `b` = count of applications. Return one row: loans, applications, and loans/applications as a % (1dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Funnel with CTEs: applications by `current_status` as a share of all applications. Return `current_status`, `share_pct` (1dp); sorted by share descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Monthly origination totals then month-on-month change. In a CTE build `month_start`, `amount` for 2024; then in the final select return `month_start`, `amount` (0dp) and `prev_amount` (0dp) using `LAG`. Sorted by `month_start`. (Previews window functions.)

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Recursive CTE number series: produce the integers 1 to 12 (column `n`) using a recursive CTE.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Recursive date spine: all month-end dates in 2025 (12 rows) starting at 2025-01-31 using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end` sorted ascending.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Reporting line depth. Using a recursive CTE walk the staff hierarchy from the top (`manager_staff_id IS NULL`) and return `depth`, `staff_count`; sorted by `depth`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Application-to-loan pipeline in 3 CTEs: `apps` (2025 applications), `settled` (those that settled), `rates` giving the settle rate. Return `applications`, `settled`, `settle_rate_pct` (1dp) as one row.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

Reuse a CTE twice: using a CTE `bal` of 2025-12-31 balances (non-closed) per loan, show the share of total balance held by the top 100 loans by balance. Return one number (`pct`, 2 dp).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Per-customer first application date, then how many customers made their first application in each year. In CTE `f` compute first `application_date` per `primary_customer_id`. Return `yr`, `new_applicants`; sorted by `yr`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Refinance chains with recursion: starting from loans with no parent (`parent_loan_id IS NULL`) that have at least one internal-refinance child, follow the child links. Return `chain_length`, `chains`, where chain_length is the number of loans in the chain from the root to the last descendant. Sorted by `chain_length`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Date spine + LEFT JOIN: for every month-end of 2025 (spine via `generate_series` or recursion) show the number of loans originated in that month, including zero months. Return `month_end`, `loans`; sorted by `month_end`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Three-step arrears story: CTE `latest` = non-closed loans at 2025-12-31 with `days_past_due`; CTE `bucketed` = bucket via CASE (`'Current'` 0, `'1-29'`, `'30-89'`, `'90+'`); final = balance and loan count per bucket. Return `bucket`, `loans`, `balance` (0dp); sorted by the bucket's severity (Current first).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Cumulative origination: CTE of monthly volume ($) by year-month for 2023, then a running total using `SUM() OVER (ORDER BY ms)`. Return `month_start`, `running_total` (0dp); sorted by `month_start`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Recursion with a ceiling: simulate a $500,000, 6.00% p.a. loan with $3,000 monthly repayments for 12 months. Return `month_no`, `balance` (2dp) for months 1-12. Balance_n = balance_{n-1} * (1 + 0.06/12) - 3000, starting at 500000 for month 0 (don't output month 0).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Consecutive-event cleanup via CTE: in `application_status_history` find applications that have exactly one 'Settled' event but more than one 'Submitted' event (duplicate loads). Return the number of such applications. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Rank-free top-N via CTE: for each `purpose`, which origination year had the most loans? Build `py` (purpose, year, count), then `mx` (max per purpose), join. Return `purpose`, `yr`, `loans`; sorted by `purpose`, `yr`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2019; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2020; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2021; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2022; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2023; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2024; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★ &nbsp; (core)

CTE of monthly loan counts for 2025; return only the months above that year's monthly average. `month_no`, `loans`; sorted by month.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

CTE + window: within `'Purchase - Owner Occupied'` loans, the 3 products with the largest total original amount. `product_id`, `total` (0 dp), `rnk`; sorted by rnk.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

CTE + window: within `'Purchase - Investment'` loans, the 3 products with the largest total original amount. `product_id`, `total` (0 dp), `rnk`; sorted by rnk.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

CTE + window: within `'Refinance'` loans, the 3 products with the largest total original amount. `product_id`, `total` (0 dp), `rnk`; sorted by rnk.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

CTE + window: within `'Equity Release / Top-up'` loans, the 3 products with the largest total original amount. `product_id`, `total` (0 dp), `rnk`; sorted by rnk.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

CTE + window: within `'Construction'` loans, the 3 products with the largest total original amount. `product_id`, `total` (0 dp), `rnk`; sorted by rnk.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Recursive date spine: all month-end dates of 2019 (12 rows) built with a recursive CTE using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end`, sorted.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Recursive date spine: all month-end dates of 2021 (12 rows) built with a recursive CTE using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end`, sorted.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Recursive date spine: all month-end dates of 2023 (12 rows) built with a recursive CTE using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end`, sorted.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Recursive date spine: all month-end dates of 2025 (12 rows) built with a recursive CTE using `last_day(prev + INTERVAL 1 MONTH)`. Return `month_end`, sorted.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Recursive CTE: the first 10 square numbers. Return `n`, `n_squared`; sorted by n.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★ &nbsp; (core)

Recursive CTE: the first 15 square numbers. Return `n`, `n_squared`; sorted by n.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★ &nbsp; (core)

Recursive CTE: the first 20 square numbers. Return `n`, `n_squared`; sorted by n.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **20 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★ &nbsp; (core)

Two-step funnel for `'Broker'` applications: CTE `a` = all applications, CTE `s` = settled ones. Return `lodged`, `settled`, `settle_pct` (1 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★ &nbsp; (core)

Two-step funnel for `'Branch'` applications: CTE `a` = all applications, CTE `s` = settled ones. Return `lodged`, `settled`, `settle_pct` (1 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★ &nbsp; (core)

Two-step funnel for `'Digital'` applications: CTE `a` = all applications, CTE `s` = settled ones. Return `lodged`, `settled`, `settle_pct` (1 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★ &nbsp; (core)

Two-step funnel for `'Mobile Lender'` applications: CTE `a` = all applications, CTE `s` = settled ones. Return `lodged`, `settled`, `settle_pct` (1 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Recursion with money: a $400,000 loan at 5.00% p.a. with $2,800 monthly repayments - the balance after 12 months (2 dp). Balance_n = balance_(n-1) * (1 + rate/12) - 2800. Return one number `balance_12`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Recursion with money: a $400,000 loan at 6.00% p.a. with $2,800 monthly repayments - the balance after 12 months (2 dp). Balance_n = balance_(n-1) * (1 + rate/12) - 2800. Return one number `balance_12`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★★ &nbsp; (challenge)

Recursion with money: a $400,000 loan at 7.00% p.a. with $2,800 monthly repayments - the balance after 12 months (2 dp). Balance_n = balance_(n-1) * (1 + rate/12) - 2800. Return one number `balance_12`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★★ &nbsp; (challenge)

Chained CTEs: `y` = loans per year; `g` = year-on-year growth % (LAG); final = years where growth exceeded 10%. `yr`, `loans`, `growth_pct` (1 dp); sorted by year.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q46 &nbsp; ★★★ &nbsp; (challenge)

Staff hierarchy path: recursive CTE from the top person producing each staff member's `depth` and a `path` string like `Top > Mgr > Employee` of full names. Return `staff_id`, `depth`, `path` for staff with depth 3, first 10 by staff_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.
