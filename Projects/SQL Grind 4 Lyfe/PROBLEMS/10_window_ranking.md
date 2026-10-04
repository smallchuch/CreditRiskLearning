# 10 - Window functions I: ROW_NUMBER, RANK, DENSE_RANK, NTILE, top-N per group

`answers/10_window_ranking/qNN.sql` &nbsp;|&nbsp; check with: `grade 10` or `grade 10 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Window functions: calculate across related rows WITHOUT collapsing them

```
 GROUP BY collapses:                       WINDOW keeps every row:
 purpose  n                                loan  purpose  amount   rank_in_purpose
 Refi     10   (one row per group)         L1    Refi     900k          1
                                           L2    Refi     700k          2
                                           L3    Constr.  400k          1
```

```
 function() OVER ( PARTITION BY group_cols     -- restart the calc for each group
                   ORDER BY sort_cols )        -- order inside the group
```

| Function | What it does | Ties |
|---|---|---|
| `ROW_NUMBER()` | 1,2,3,4 unique | broken arbitrarily (add a tie-breaker column!) |
| `RANK()` | 1,2,2,4 gaps | same rank |
| `DENSE_RANK()` | 1,2,2,3 no gaps | same rank |
| `NTILE(4)` | quartile number | - |
| `PERCENT_RANK()` | 0..1 | - |

**Top-N per group** is the classic use:
```
 SELECT * FROM (SELECT ..., ROW_NUMBER() OVER (PARTITION BY purpose ORDER BY original_amount DESC, loan_id) AS rn FROM loan)
 WHERE rn <= 3
```
(DuckDB also lets you write `QUALIFY rn <= 3` to filter on a window result directly.)

You cannot use a window function inside `WHERE` - wrap in a subquery/CTE or use `QUALIFY`.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Number the 10 largest loans: `loan_id`, `original_amount`, `rn` (ROW_NUMBER ordered by amount DESC, then loan_id). Return rows with rn <= 10, sorted by rn.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Rank products by number of loans (RANK, highest = 1). Return `product_id`, `loans`, `rnk`; sorted by `rnk`, `product_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

For the first 12 loans by `loan_id`, add a running row number `rn` across all of them. Return `loan_id`, `rn`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Largest loan per `purpose` (top-1 per group, ROW_NUMBER with tie-break by `loan_id`). Return `purpose`, `loan_id`, `original_amount`; sorted by `purpose`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Top 3 loans per `channel` by `original_amount` (tie-break `loan_id`). Return `channel`, `loan_id`, `original_amount`, `rn`; sorted by `channel`, `rn`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Each customer's FIRST loan: for each primary customer return the earliest loan (`loan_id`, `origination_date`), ties broken by `loan_id`. Count how many customers' first loan was in each `purpose`. Return `purpose`, `customers`; sorted by customers descending then purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

RANK vs DENSE_RANK: for loan amounts rounded to the nearest $100,000 (`ROUND(original_amount,-5)`) among loans 1-30, return `loan_id`, rounded amount, `rank` and `dense_rank` (descending). Sorted by `rank`, `loan_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Quartiles: using `NTILE(4)` over all loans ordered by `original_amount` (then loan_id), return the minimum and maximum amount per quartile. Return `quartile`, `min_amount`, `max_amount`; sorted by `quartile`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Use `QUALIFY`: the largest balance loan per property state at 2025-12-31 (non-closed). Return `state`, `loan_id`, `closing_balance`; sorted by `state`. Tie-break `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Latest record per entity: `application_status_history` has multiple events per application. Return the LAST status (by `status_ts`, then `event_id`) for applications 1-15. `application_id`, `status`; sorted by `application_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Broker league table: rank brokers by total original lending within each `aggregator` (dense). Return `aggregator`, `broker_id`, `total` (0dp), `rnk` for rank <= 2; sorted by `aggregator`, `rnk`, `broker_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

Percentage rank of each product by average rate: return `product_id`, `avg_rate` (3dp) and `PERCENT_RANK()` ordered by average rate (2dp). Sorted by `product_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

De-duplicate customers: the `customer` table has duplicate people (same lower/trimmed name + date_of_birth, ignoring NULL DOB). Number duplicates within each person with ROW_NUMBER ordered by `customer_id`, then count how many extra (rn > 1) rows exist. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Keep the cleanest status event: in `application_status_history` some events are duplicated with a later `loaded_at`. For each (`application_id`, `status`) keep the row with the EARLIEST `loaded_at` (tie `event_id`). Count rows after de-duplication. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Second-largest loan per purpose (not the largest). Return `purpose`, `loan_id`, `original_amount`; sorted by `purpose`. Tie-break `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Top 5% by balance: using `NTILE(20)` on non-closed loan balances at 2025-12-31 (ordered by `closing_balance`, `loan_id`), count loans in the top bucket (20) and the share of balance they hold (1dp %). Return `loans`, `share_pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

First arrears event per loan: the earliest `snapshot_date` where `days_past_due >= 30` for each loan. Return the count of loans that ever hit 30+ DPD and the earliest such date overall. Two columns: `loans`, `earliest_date`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Rank within a rank: for each `state` (customer.state cleaned = `UPPER(TRIM(state))` limited to the 8 clean codes) find the top-3 `last_name` by number of customers (ties: alphabetical). Return `state`, `last_name`, `customers`, `rn`; sorted by `state`, `rn`. Only for states 'SA' and 'WA'.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Staff productivity decile: count loans assessed per assessor, then NTILE(10) them by count (ties by staff_id). Return `decile`, `assessors`, `avg_loans` (1dp); sorted by `decile`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Gaps-free sequence check: loans ranked by `loan_id` - confirm `ROW_NUMBER() OVER (ORDER BY loan_id)` equals `loan_id` for all loans (no gaps). Return the count of loans where they differ. One number (0 means no gaps).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

For `'Purchase - Owner Occupied'` loans: the 2 largest loans in each `channel` (ties by `loan_id`). `channel`, `loan_id`, `original_amount`, `rn`; sorted by channel, rn.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★ &nbsp; (core)

For `'Purchase - Investment'` loans: the 2 largest loans in each `channel` (ties by `loan_id`). `channel`, `loan_id`, `original_amount`, `rn`; sorted by channel, rn.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★ &nbsp; (core)

For `'Refinance'` loans: the 2 largest loans in each `channel` (ties by `loan_id`). `channel`, `loan_id`, `original_amount`, `rn`; sorted by channel, rn.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★ &nbsp; (core)

For `'Equity Release / Top-up'` loans: the 2 largest loans in each `channel` (ties by `loan_id`). `channel`, `loan_id`, `original_amount`, `rn`; sorted by channel, rn.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★★ &nbsp; (core)

For `'Construction'` loans: the 2 largest loans in each `channel` (ties by `loan_id`). `channel`, `loan_id`, `original_amount`, `rn`; sorted by channel, rn.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2019 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2020 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2021 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2022 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2023 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2024 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Rank products by number of loans originated in 2025 using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Quartiles of `'Broker'` loan amounts: `NTILE(4)` over `original_amount` (tie `loan_id`); return per quartile the loan count, min and max amount. `quartile`, `loans`, `min_amount`, `max_amount`; sorted by quartile.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Quartiles of `'Branch'` loan amounts: `NTILE(4)` over `original_amount` (tie `loan_id`); return per quartile the loan count, min and max amount. `quartile`, `loans`, `min_amount`, `max_amount`; sorted by quartile.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Quartiles of `'Digital'` loan amounts: `NTILE(4)` over `original_amount` (tie `loan_id`); return per quartile the loan count, min and max amount. `quartile`, `loans`, `min_amount`, `max_amount`; sorted by quartile.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★ &nbsp; (core)

Quartiles of `'Mobile Lender'` loan amounts: `NTILE(4)` over `original_amount` (tie `loan_id`); return per quartile the loan count, min and max amount. `quartile`, `loans`, `min_amount`, `max_amount`; sorted by quartile.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Dense rank branches in `'NSW'` by loans originated (most = 1); show ranks 1-3. `branch_name`, `loans`, `drnk`; sorted by drnk, branch_name.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Dense rank branches in `'VIC'` by loans originated (most = 1); show ranks 1-3. `branch_name`, `loans`, `drnk`; sorted by drnk, branch_name.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Dense rank branches in `'QLD'` by loans originated (most = 1); show ranks 1-3. `branch_name`, `loans`, `drnk`; sorted by drnk, branch_name.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Dense rank branches in `'SA'` by loans originated (most = 1); show ranks 1-3. `branch_name`, `loans`, `drnk`; sorted by drnk, branch_name.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Dense rank branches in `'WA'` by loans originated (most = 1); show ranks 1-3. `branch_name`, `loans`, `drnk`; sorted by drnk, branch_name.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Each customer's most recent application up to the end of 2020 (latest `application_date`, tie `application_id`): count how many of those latest applications were `'Declined'`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Each customer's most recent application up to the end of 2022 (latest `application_date`, tie `application_id`): count how many of those latest applications were `'Declined'`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★★ &nbsp; (challenge)

Each customer's most recent application up to the end of 2024 (latest `application_date`, tie `application_id`): count how many of those latest applications were `'Declined'`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★★ &nbsp; (challenge)

Top 1 per `purpose`: the 1 loans with the highest `lvr_at_origination_pct` in each purpose (ties by `loan_id`). Return `purpose`, `loan_id`, `lvr_at_origination_pct`; sorted by purpose, then LVR descending, then loan_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q46 &nbsp; ★★★ &nbsp; (challenge)

Top 3 per `purpose`: the 3 loans with the highest `lvr_at_origination_pct` in each purpose (ties by `loan_id`). Return `purpose`, `loan_id`, `lvr_at_origination_pct`; sorted by purpose, then LVR descending, then loan_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **18 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q47 &nbsp; ★★★ &nbsp; (challenge)

Top 5 per `purpose`: the 5 loans with the highest `lvr_at_origination_pct` in each purpose (ties by `loan_id`). Return `purpose`, `loan_id`, `lvr_at_origination_pct`; sorted by purpose, then LVR descending, then loan_id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q48 &nbsp; ★★ &nbsp; (core)

Percentile rank of loans originated in 2021: the 5 loans with the highest `PERCENT_RANK()` by original amount (ties by loan_id). `loan_id`, `original_amount`, `pct_rank` (4 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q49 &nbsp; ★★ &nbsp; (core)

Percentile rank of loans originated in 2023: the 5 loans with the highest `PERCENT_RANK()` by original amount (ties by loan_id). `loan_id`, `original_amount`, `pct_rank` (4 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q50 &nbsp; ★★ &nbsp; (core)

Percentile rank of loans originated in 2025: the 5 loans with the highest `PERCENT_RANK()` by original amount (ties by loan_id). `loan_id`, `original_amount`, `pct_rank` (4 dp).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.
