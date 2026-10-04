from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="10_window_ranking", title="10 - Window functions I: ROW_NUMBER, RANK, DENSE_RANK, NTILE, top-N per group", primer=PRIMER, problems=[
    P(1, "Number the 10 largest loans: `loan_id`, `original_amount`, `rn` (ROW_NUMBER ordered by amount DESC, then loan_id). Return rows with rn <= 10, sorted by rn.",
      "SELECT * FROM (SELECT loan_id, original_amount, ROW_NUMBER() OVER (ORDER BY original_amount DESC, loan_id) AS rn FROM loan) WHERE rn <= 10 ORDER BY rn"),
    P(1, "Rank products by number of loans (RANK, highest = 1). Return `product_id`, `loans`, `rnk`; sorted by `rnk`, `product_id`.",
      "SELECT product_id, COUNT(*) AS n, RANK() OVER (ORDER BY COUNT(*) DESC) AS r FROM loan GROUP BY 1 ORDER BY r, 1"),
    P(1, "For the first 12 loans by `loan_id`, add a running row number `rn` across all of them. Return `loan_id`, `rn`; sorted by `loan_id`.",
      "SELECT loan_id, ROW_NUMBER() OVER (ORDER BY loan_id) FROM (SELECT loan_id FROM loan ORDER BY loan_id LIMIT 12) ORDER BY 1"),
    P(2, "Largest loan per `purpose` (top-1 per group, ROW_NUMBER with tie-break by `loan_id`). Return `purpose`, `loan_id`, `original_amount`; sorted by `purpose`.",
      "SELECT purpose, loan_id, original_amount FROM (SELECT purpose, loan_id, original_amount, ROW_NUMBER() OVER (PARTITION BY purpose ORDER BY original_amount DESC, loan_id) AS rn FROM loan) WHERE rn=1 ORDER BY 1"),
    P(2, "Top 3 loans per `channel` by `original_amount` (tie-break `loan_id`). Return `channel`, `loan_id`, `original_amount`, `rn`; sorted by `channel`, `rn`.",
      "SELECT channel, loan_id, original_amount, rn FROM (SELECT channel, loan_id, original_amount, ROW_NUMBER() OVER (PARTITION BY channel ORDER BY original_amount DESC, loan_id) AS rn FROM loan) WHERE rn<=3 ORDER BY 1, rn"),
    P(2, "Each customer's FIRST loan: for each primary customer return the earliest loan (`loan_id`, `origination_date`), ties broken by `loan_id`. Count how many customers' first loan was in each `purpose`. Return `purpose`, `customers`; sorted by customers descending then purpose.",
      "SELECT purpose, COUNT(*) AS n FROM (SELECT purpose, ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY origination_date, loan_id) AS rn FROM loan) WHERE rn=1 GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "RANK vs DENSE_RANK: for loan amounts rounded to the nearest $100,000 (`ROUND(original_amount,-5)`) among loans 1-30, return `loan_id`, rounded amount, `rank` and `dense_rank` (descending). Sorted by `rank`, `loan_id`.",
      "SELECT loan_id, a, RANK() OVER (ORDER BY a DESC), DENSE_RANK() OVER (ORDER BY a DESC) FROM (SELECT loan_id, ROUND(original_amount,-5) AS a FROM loan WHERE loan_id <= 30) ORDER BY 3, 1"),
    P(2, "Quartiles: using `NTILE(4)` over all loans ordered by `original_amount` (then loan_id), return the minimum and maximum amount per quartile. Return `quartile`, `min_amount`, `max_amount`; sorted by `quartile`.",
      "SELECT q, MIN(original_amount), MAX(original_amount) FROM (SELECT original_amount, NTILE(4) OVER (ORDER BY original_amount, loan_id) AS q FROM loan) GROUP BY 1 ORDER BY 1"),
    P(2, "Use `QUALIFY`: the largest balance loan per property state at 2025-12-31 (non-closed). Return `state`, `loan_id`, `closing_balance`; sorted by `state`. Tie-break `loan_id`.",
      """SELECT d.state, s.loan_id, s.closing_balance FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed'
QUALIFY ROW_NUMBER() OVER (PARTITION BY d.state ORDER BY s.closing_balance DESC, s.loan_id)=1 ORDER BY 1"""),
    P(2, "Latest record per entity: `application_status_history` has multiple events per application. Return the LAST status (by `status_ts`, then `event_id`) for applications 1-15. `application_id`, `status`; sorted by `application_id`.",
      "SELECT application_id, status FROM application_status_history WHERE application_id <= 15 QUALIFY ROW_NUMBER() OVER (PARTITION BY application_id ORDER BY status_ts DESC, event_id DESC)=1 ORDER BY 1"),
    P(2, "Broker league table: rank brokers by total original lending within each `aggregator` (dense). Return `aggregator`, `broker_id`, `total` (0dp), `rnk` for rank <= 2; sorted by `aggregator`, `rnk`, `broker_id`.",
      """SELECT * FROM (SELECT b.aggregator, b.broker_id, ROUND(SUM(l.original_amount),0) AS t, DENSE_RANK() OVER (PARTITION BY b.aggregator ORDER BY SUM(l.original_amount) DESC) AS r
FROM loan l JOIN dim_broker b USING (broker_id) GROUP BY 1,2) WHERE r<=2 ORDER BY 1, 4, 2"""),
    P(2, "Percentage rank of each product by average rate: return `product_id`, `avg_rate` (3dp) and `PERCENT_RANK()` ordered by average rate (2dp). Sorted by `product_id`.",
      "SELECT product_id, ROUND(AVG(interest_rate_at_origination_pct),3), ROUND(PERCENT_RANK() OVER (ORDER BY AVG(interest_rate_at_origination_pct)),2) FROM loan GROUP BY 1 ORDER BY 1"),
    P(3, "De-duplicate customers: the `customer` table has duplicate people (same lower/trimmed name + date_of_birth, ignoring NULL DOB). Number duplicates within each person with ROW_NUMBER ordered by `customer_id`, then count how many extra (rn > 1) rows exist. One number.",
      "SELECT COUNT(*) FROM (SELECT ROW_NUMBER() OVER (PARTITION BY LOWER(TRIM(first_name)), LOWER(TRIM(last_name)), date_of_birth ORDER BY customer_id) AS rn FROM customer WHERE date_of_birth IS NOT NULL) WHERE rn>1"),
    P(3, "Keep the cleanest status event: in `application_status_history` some events are duplicated with a later `loaded_at`. For each (`application_id`, `status`) keep the row with the EARLIEST `loaded_at` (tie `event_id`). Count rows after de-duplication. One number.",
      "SELECT COUNT(*) FROM (SELECT 1 FROM application_status_history QUALIFY ROW_NUMBER() OVER (PARTITION BY application_id, status ORDER BY loaded_at, event_id)=1)"),
    P(3, "Second-largest loan per purpose (not the largest). Return `purpose`, `loan_id`, `original_amount`; sorted by `purpose`. Tie-break `loan_id`.",
      "SELECT purpose, loan_id, original_amount FROM loan QUALIFY ROW_NUMBER() OVER (PARTITION BY purpose ORDER BY original_amount DESC, loan_id)=2 ORDER BY 1"),
    P(3, "Top 5% by balance: using `NTILE(20)` on non-closed loan balances at 2025-12-31 (ordered by `closing_balance`, `loan_id`), count loans in the top bucket (20) and the share of balance they hold (1dp %). Return `loans`, `share_pct`.",
      """WITH b AS (SELECT closing_balance AS x, NTILE(20) OVER (ORDER BY closing_balance, loan_id) AS q FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed')
SELECT COUNT(*) FILTER (WHERE q=20), ROUND(100*SUM(x) FILTER (WHERE q=20)/SUM(x),1) FROM b"""),
    P(3, "First arrears event per loan: the earliest `snapshot_date` where `days_past_due >= 30` for each loan. Return the count of loans that ever hit 30+ DPD and the earliest such date overall. Two columns: `loans`, `earliest_date`.",
      "SELECT COUNT(*), MIN(d) FROM (SELECT loan_id, MIN(snapshot_date) AS d FROM loan_monthly_snapshot WHERE days_past_due>=30 GROUP BY 1)"),
    P(3, "Rank within a rank: for each `state` (customer.state cleaned = `UPPER(TRIM(state))` limited to the 8 clean codes) find the top-3 `last_name` by number of customers (ties: alphabetical). Return `state`, `last_name`, `customers`, `rn`; sorted by `state`, `rn`. Only for states 'SA' and 'WA'.",
      """SELECT * FROM (SELECT UPPER(TRIM(state)) AS st, last_name, COUNT(*) AS n, ROW_NUMBER() OVER (PARTITION BY UPPER(TRIM(state)) ORDER BY COUNT(*) DESC, last_name) AS rn
FROM customer WHERE UPPER(TRIM(state)) IN ('SA','WA') GROUP BY 1,2) WHERE rn<=3 ORDER BY 1, 4"""),
    P(3, "Staff productivity decile: count loans assessed per assessor, then NTILE(10) them by count (ties by staff_id). Return `decile`, `assessors`, `avg_loans` (1dp); sorted by `decile`.",
      """WITH c AS (SELECT assessor_staff_id, COUNT(*) AS n FROM loan GROUP BY 1), t AS (SELECT n, NTILE(10) OVER (ORDER BY n, assessor_staff_id) AS d FROM c)
SELECT d, COUNT(*), ROUND(AVG(n),1) FROM t GROUP BY 1 ORDER BY 1"""),
    P(3, "Gaps-free sequence check: loans ranked by `loan_id` - confirm `ROW_NUMBER() OVER (ORDER BY loan_id)` equals `loan_id` for all loans (no gaps). Return the count of loans where they differ. One number (0 means no gaps).",
      "SELECT COUNT(*) FROM (SELECT loan_id, ROW_NUMBER() OVER (ORDER BY loan_id) AS rn FROM loan) WHERE rn <> loan_id"),
])
