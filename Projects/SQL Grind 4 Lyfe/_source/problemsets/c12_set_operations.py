from . import P

PRIMER = r"""
## Set operations stack results vertically (joins glue sideways)

```
 Query A (3 rows)         Query B (3 rows)
 +----+                   +----+
 | 1  |                   | 2  |
 | 2  |                   | 3  |
 | 3  |                   | 4  |
 +----+                   +----+

 UNION ALL  -> 1,2,3,2,3,4   (keep everything)
 UNION      -> 1,2,3,4       (remove duplicates)
 INTERSECT  -> 2,3           (in both)
 EXCEPT     -> 1             (in A but not B)
```

Rules: same number of columns, compatible types, column names come from the **first** query.
`UNION ALL` is faster and what you want when you know there are no dupes (or want them).
`EXCEPT` is a clean way to reconcile: "what is in source A that is missing from B?"

Common credit-risk uses: stacking monthly extracts, reconciling two systems, finding customers in one product but not another.
"""

CONCEPT = dict(id="12_set_operations", title="12 - UNION, INTERSECT, EXCEPT", primer=PRIMER, problems=[
    P(1, "Stack two lists: `product_id`s 1-3 UNION ALL product_ids 3-5 from `dim_product`. Return `product_id` sorted ascending (3 appears twice).",
      "SELECT product_id FROM dim_product WHERE product_id <= 3 UNION ALL SELECT product_id FROM dim_product WHERE product_id BETWEEN 3 AND 5 ORDER BY 1"),
    P(1, "Same lists with `UNION` (dedupe). Return `product_id` sorted.",
      "SELECT product_id FROM dim_product WHERE product_id <= 3 UNION SELECT product_id FROM dim_product WHERE product_id BETWEEN 3 AND 5 ORDER BY 1"),
    P(1, "Customers who are primary on BOTH a 'Purchase - Owner Occupied' loan AND a 'Purchase - Investment' loan (INTERSECT). Count them. One number.",
      "SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE purpose='Purchase - Owner Occupied' INTERSECT SELECT primary_customer_id FROM loan WHERE purpose='Purchase - Investment')"),
    P(2, "Customers who applied (primary) but never got a loan (EXCEPT). Count them. One number.",
      "SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application EXCEPT SELECT primary_customer_id FROM loan)"),
    P(2, "A combined events feed: UNION ALL of `loan_event` (loan_id, event_date, event_type) and hardship starts (loan_id, start_date, 'Hardship start') for loans 1-300. Return `loan_id`, `event_date`, `event_type`, sorted by `loan_id`, `event_date`, `event_type`.",
      "SELECT loan_id, event_date, event_type FROM (SELECT loan_id, event_date, event_type FROM loan_event WHERE loan_id <= 300 UNION ALL SELECT loan_id, start_date, 'Hardship start' FROM hardship_arrangement WHERE loan_id <= 300) ORDER BY 1,2,3"),
    P(2, "Customers that appear in the `complaint` table but have NO loan as primary or co-borrower. Use EXCEPT on `customer_id` vs `loan_borrower.customer_id`. Count them. (May be 0.)",
      "SELECT COUNT(*) FROM (SELECT customer_id FROM complaint EXCEPT SELECT customer_id FROM loan_borrower)"),
    P(2, "One list of every person-ish key: UNION of `primary_customer_id` from `loan_application` and `customer_id` from `application_applicant`. How many distinct customer ids? One number.",
      "SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application UNION SELECT customer_id FROM application_applicant)"),
    P(2, "Applications with a bureau report but no assessment row (EXCEPT on application_id). Count. One number (expect 0).",
      "SELECT COUNT(*) FROM (SELECT application_id FROM credit_bureau_report EXCEPT SELECT application_id FROM application_assessment)"),
    P(2, "Reconcile loans to snapshots: loans with no rows in `loan_monthly_snapshot` (EXCEPT). Count them. One number.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan EXCEPT SELECT loan_id FROM loan_monthly_snapshot)"),
    P(2, "Reconcile loan status: loans marked `'Closed'` on `loan` but whose latest snapshot status is NOT 'Closed' (EXCEPT of loan_ids). Count. One number (expect 0).",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan WHERE loan_status='Closed' EXCEPT SELECT loan_id FROM loan_monthly_snapshot WHERE loan_status='Closed')"),
    P(3, "Add a total row: per `channel` loan counts, UNION ALL a 'ALL' row with the grand total. Return `channel`, `loans`; sorted with channels alphabetically and 'ALL' last (hint: sort by `channel = 'ALL'`, then channel).",
      "SELECT channel, loans FROM (SELECT channel, COUNT(*) AS loans FROM loan GROUP BY 1 UNION ALL SELECT 'ALL', COUNT(*) FROM loan) ORDER BY channel='ALL', channel"),
    P(3, "Loans in recovery or with a loss record: UNION of loan_ids from `loan_loss` and loans with `loan_status='In Recovery'`. Count the union. One number.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan_loss UNION SELECT loan_id FROM loan WHERE loan_status='In Recovery')"),
    P(3, "Symmetric difference: customers in `customer` whose cleaned (lowercase) email appears more than once vs customers with a mobile starting '+61'. How many customers appear in exactly ONE of the two groups? Use UNION of two EXCEPTs. One number.",
      """WITH a AS (SELECT customer_id FROM customer WHERE email IS NOT NULL AND LOWER(email) IN (SELECT LOWER(email) FROM customer WHERE email IS NOT NULL GROUP BY 1 HAVING COUNT(*)>1)),
b AS (SELECT customer_id FROM customer WHERE mobile LIKE '+61%')
SELECT COUNT(*) FROM (SELECT * FROM (SELECT * FROM a EXCEPT SELECT * FROM b) UNION SELECT * FROM (SELECT * FROM b EXCEPT SELECT * FROM a))"""),
    P(3, "Month-by-month stack: UNION ALL 2023, 2024 and 2025 loan counts per month number into one table of `yr`, `mon`, `loans`. Return the rows for months 1-3 only, sorted by `yr`, `mon`.",
      """SELECT yr, mon, loans FROM (SELECT 2023 AS yr, month(origination_date) AS mon, COUNT(*) AS loans FROM loan WHERE year(origination_date)=2023 GROUP BY 2
UNION ALL SELECT 2024, month(origination_date), COUNT(*) FROM loan WHERE year(origination_date)=2024 GROUP BY 2
UNION ALL SELECT 2025, month(origination_date), COUNT(*) FROM loan WHERE year(origination_date)=2025 GROUP BY 2) WHERE mon <= 3 ORDER BY 1,2"""),
    P(3, "Funnel as a stack: one result with `stage` and `apps` using UNION ALL: 'Lodged' = all applications; 'Decided' = decision not null; 'Approved' = decision Approved; 'Settled' = current_status Settled. Sorted by `apps` descending.",
      """SELECT stage, apps FROM (SELECT 'Lodged' AS stage, COUNT(*) AS apps FROM loan_application UNION ALL SELECT 'Decided', COUNT(*) FROM loan_application WHERE decision IS NOT NULL
UNION ALL SELECT 'Approved', COUNT(*) FROM loan_application WHERE decision='Approved' UNION ALL SELECT 'Settled', COUNT(*) FROM loan_application WHERE current_status='Settled') ORDER BY apps DESC"""),
    P(3, "INTERSECT with multiple columns: (`purpose`, `channel`) combinations that appear both in `loan` and in `loan_application`. Return the pairs sorted by purpose, channel.",
      "SELECT purpose, channel FROM loan INTERSECT SELECT purpose, channel FROM loan_application ORDER BY 1,2"),
])
