from . import P

PRIMER = r"""
## A JOIN lines up rows from two tables using a matching key

```
 loan                         dim_product
 loan_id | product_id         product_id | product_name
    1    |    4        ------>     4     | Standard Variable - Investment P&I
    2    |    9        ------>     9     | Fixed 3 Year - Owner Occupied

 SELECT l.loan_id, p.product_name
 FROM   loan l
 JOIN   dim_product p ON p.product_id = l.product_id
```

```
 INNER JOIN   only rows that match on BOTH sides
 LEFT  JOIN   all left rows; right columns NULL when there is no match
 RIGHT JOIN   mirror of LEFT (rarely needed - swap the tables instead)
 FULL  JOIN   everything from both sides
 CROSS JOIN   every left row paired with every right row (a deliberate grid)
```

```
        INNER           LEFT              FULL
       (  A ( X ) B )    ( A ( X ) b )    ( A ( X ) B )
        only overlap     all A + overlap   everything
```

### Habits that keep you out of trouble
* Always alias tables (`l`, `a`, `p`) and prefix columns (`l.loan_id`).
* Know the **grain** of each table (one row per what?). Joining to a table at a finer grain multiplies rows.
* After joining, sanity-check `COUNT(*)` against what you expect.
* `JOIN ... USING (col)` is shorthand when both columns share the name.
* Put filters on the **right** table of a LEFT JOIN in the `ON` clause, or the join silently becomes an inner join.

Grain cheat-sheet: `loan` 1/loan | `loan_borrower` 1/loan-per-borrower | `loan_monthly_snapshot` 1/loan-per-month | `loan_security` 1/loan-per-security | `customer` 1/person (with some duplicates!)
"""

CONCEPT = dict(id="06_joins_basic", title="06 - JOINs: inner, left, multiple tables", primer=PRIMER, problems=[
    P(1, "Loans with their product name: `loan_id`, `product_name` for loans 1-10, sorted by `loan_id`.",
      "SELECT l.loan_id, p.product_name FROM loan l JOIN dim_product p ON p.product_id=l.product_id WHERE l.loan_id <= 10 ORDER BY l.loan_id"),
    P(1, "Number of loans per `product_name`. Return `product_name`, `loans`; sorted by `loans` descending then `product_name`.",
      "SELECT p.product_name, COUNT(*) AS n FROM loan l JOIN dim_product p USING (product_id) GROUP BY 1 ORDER BY n DESC, 1"),
    P(1, "Loans 1-10 with the primary borrower's surname: `loan_id`, `last_name`. Join `loan` to `customer` on `primary_customer_id`. Sorted by `loan_id`.",
      "SELECT l.loan_id, c.last_name FROM loan l JOIN customer c ON c.customer_id=l.primary_customer_id WHERE l.loan_id <= 10 ORDER BY l.loan_id"),
    P(1, "Loans 1-10 and the branch name that wrote them (`dim_branch`). Use a LEFT JOIN so loans with no branch still appear (branch_name NULL). Return `loan_id`, `branch_name`; sorted by `loan_id`.",
      "SELECT l.loan_id, b.branch_name FROM loan l LEFT JOIN dim_branch b ON b.branch_id=l.branch_id WHERE l.loan_id <= 10 ORDER BY l.loan_id"),
    P(1, "Count of loans per state of the property: join `loan` -> `property` -> `dim_postcode`. Return `state`, `loans`; sorted by `state`.",
      "SELECT d.state, COUNT(*) FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode GROUP BY 1 ORDER BY 1"),
    P(2, "Co-borrowers: number of loans with exactly 2 borrowers on `loan_borrower`. One number.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan_borrower GROUP BY 1 HAVING COUNT(*) = 2)"),
    P(2, "Loans with the broker firm and aggregator for Broker-channel loans 1-200 that have a broker: `loan_id`, `firm_name`, `aggregator`; sorted by `loan_id`.",
      "SELECT l.loan_id, b.firm_name, b.aggregator FROM loan l JOIN dim_broker b ON b.broker_id=l.broker_id WHERE l.channel='Broker' AND l.loan_id <= 200 ORDER BY l.loan_id"),
    P(2, "Total original amount by aggregator. Return `aggregator`, `total_amount` (0 dp); sorted by `total_amount` descending.",
      "SELECT b.aggregator, ROUND(SUM(l.original_amount),0) AS t FROM loan l JOIN dim_broker b ON b.broker_id=l.broker_id GROUP BY 1 ORDER BY t DESC"),
    P(2, "The assessor behind each loan: count loans by assessor `team` (join `dim_staff` on `assessor_staff_id`). Return `team`, `loans`; sorted by `loans` descending then `team`.",
      "SELECT s.team, COUNT(*) AS n FROM loan l JOIN dim_staff s ON s.staff_id=l.assessor_staff_id GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "Loan-level LVR cross-check: join `loan` to `loan_application` on `application_id`. For loans 1-10 return `loan_id`, `requested_amount`, `original_amount` (the loan may be resized). Sorted by `loan_id`.",
      "SELECT l.loan_id, a.requested_amount, l.original_amount FROM loan l JOIN loan_application a ON a.application_id=l.application_id WHERE l.loan_id <= 10 ORDER BY l.loan_id"),
    P(2, "Declined applications with the reason description: `application_id`, `reason_description` for applications 1-60 with `decision='Declined'`. Join `ref_decline_reason` on code. Sorted by `application_id`.",
      "SELECT a.application_id, r.reason_description FROM loan_application a JOIN ref_decline_reason r ON r.reason_code=a.decline_reason_code WHERE a.decision='Declined' AND a.application_id <= 60 ORDER BY 1"),
    P(2, "Decline reasons by category: `reason_category`, `declined_apps`; sorted by count descending then category.",
      "SELECT r.reason_category, COUNT(*) AS n FROM loan_application a JOIN ref_decline_reason r ON r.reason_code=a.decline_reason_code GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "Arrears bucket labels. Using `ref_arrears_bucket` joined on `days_past_due BETWEEN dpd_from AND COALESCE(dpd_to, 99999)` count non-closed loans at 2025-12-31 per `bucket_name`. Return `bucket_name`, `loans`; sorted by `bucket_id`.",
      "SELECT b.bucket_name, COUNT(*) FROM loan_monthly_snapshot s JOIN ref_arrears_bucket b ON s.days_past_due BETWEEN b.dpd_from AND COALESCE(b.dpd_to, 99999) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY b.bucket_id, b.bucket_name ORDER BY b.bucket_id"),
    P(2, "Hardship by team: join `hardship_arrangement` to `loan` and count arrangements per loan `purpose`. Return `purpose`, `arrangements`; sorted by `arrangements` descending then `purpose`.",
      "SELECT l.purpose, COUNT(*) AS n FROM hardship_arrangement h JOIN loan l USING (loan_id) GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "Complaints with their loan product: count complaints per `product_name` (some complaints have no loan - drop them). Return `product_name`, `complaints`; sorted by `complaints` descending then `product_name`.",
      "SELECT p.product_name, COUNT(*) AS n FROM complaint c JOIN loan l ON l.loan_id=c.loan_id JOIN dim_product p ON p.product_id=l.product_id GROUP BY 1 ORDER BY n DESC, 1"),
    P(3, "LEFT JOIN trap. Customers 1-30 with the number of loans they are primary on - customers with no loan must show 0. Return `customer_id`, `loans`; sorted by `customer_id`.",
      "SELECT c.customer_id, COUNT(l.loan_id) FROM customer c LEFT JOIN loan l ON l.primary_customer_id=c.customer_id WHERE c.customer_id <= 30 GROUP BY 1 ORDER BY 1",
      hint="`COUNT(l.loan_id)` counts matches only; `COUNT(*)` would give 1 for the no-match customers."),
    P(3, "Valuation at origination vs now: for loans 1-10 return `loan_id`, `security_value_at_origination`, and the latest `valuation_amount` for the loan's property from `property_valuation` with `valuation_date <= 2025-12-31` that is > 0 (AVM zeros are bad data). Sorted by `loan_id`. Use a subquery or join on MAX(valuation_date).",
      """SELECT l.loan_id, l.security_value_at_origination, v.valuation_amount FROM loan l
JOIN property_valuation v ON v.property_id=l.property_id
WHERE l.loan_id <= 10 AND v.valuation_amount > 0
  AND v.valuation_date = (SELECT MAX(v2.valuation_date) FROM property_valuation v2 WHERE v2.property_id=l.property_id AND v2.valuation_amount>0 AND v2.valuation_date <= DATE '2025-12-31')
ORDER BY l.loan_id""", order=True),
    P(3, "Join through the application: for approved-and-settled applications in 2025 (`current_status='Settled'`, `application_date` in 2025) show average bureau score (join `credit_bureau_report` on application_id and customer = primary customer) per `channel`, 0 dp. Return `channel`, `avg_score`; sorted by `channel`.",
      "SELECT a.channel, ROUND(AVG(b.bureau_score),0) FROM loan_application a JOIN credit_bureau_report b ON b.application_id=a.application_id AND b.customer_id=a.primary_customer_id WHERE a.current_status='Settled' AND a.application_date >= DATE '2025-01-01' AND a.application_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1"),
    P(3, "Income per application: `application_income` = SUM of `COALESCE(verified, declared)` across `applicant_income`. Return average per `channel` (0 dp) for applications in 2025. Return `channel`, `avg_income`; sorted by `channel`. (Watch the grain: sum incomes per application first, then average.)",
      """SELECT a.channel, ROUND(AVG(i.inc),0) FROM loan_application a JOIN (SELECT application_id, SUM(COALESCE(verified_annual_amount, declared_annual_amount)) AS inc FROM applicant_income GROUP BY 1) i USING (application_id)
WHERE a.application_date >= DATE '2025-01-01' AND a.application_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1"""),
    P(3, "Month-end calendar join: for each month-end `snapshot_date` in 2025 list `snapshot_date` and its `day_name` from `dim_date` (distinct dates only). Sorted by date.",
      "SELECT DISTINCT s.snapshot_date, d.day_name FROM loan_monthly_snapshot s JOIN dim_date d ON d.full_date=s.snapshot_date WHERE s.snapshot_date >= DATE '2025-01-01' ORDER BY 1"),
    P(3, "Brokers who wrote no loans at all (LEFT JOIN, filter NULL on the right). Return `broker_id`, `firm_name`, sorted by `broker_id`.",
      "SELECT b.broker_id, b.firm_name FROM dim_broker b LEFT JOIN loan l ON l.broker_id=b.broker_id WHERE l.loan_id IS NULL ORDER BY 1", empty_ok=True),
])
