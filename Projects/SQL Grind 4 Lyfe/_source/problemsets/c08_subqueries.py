from . import P

PRIMER = r"""
## A subquery is a query inside a query - think "the answer to a smaller question"

```
 "Loans bigger than the average loan"

   SELECT loan_id FROM loan
   WHERE original_amount > ( SELECT AVG(original_amount) FROM loan )
                           \_____ scalar subquery: returns ONE value ____/
```

| Where | Returns | Example |
|---|---|---|
| `WHERE x > (subq)` | one value | above-average |
| `WHERE x IN (subq)` | a list | customers in a set |
| `WHERE EXISTS (subq)` | yes/no per row | has a related row |
| `FROM (subq) t` | a table | pre-aggregate then reuse |
| `SELECT (subq)` | one value per row | rarely - slow |

**Correlated subquery** - the inner query refers to the outer row, so it re-runs per row logically:
```
 WHERE original_amount > (SELECT AVG(original_amount) FROM loan i WHERE i.purpose = o.purpose)
```
means "above the average *of its own purpose*". Often a window function is the cleaner modern alternative.

**Beware** `NOT IN` with NULLs - use `NOT EXISTS`.
"""

CONCEPT = dict(id="08_subqueries", title="08 - Subqueries: scalar, IN, EXISTS, correlated, derived tables", primer=PRIMER, problems=[
    P(1, "Loans with an original amount above the average original amount. Count them. One number.",
      "SELECT COUNT(*) FROM loan WHERE original_amount > (SELECT AVG(original_amount) FROM loan)"),
    P(1, "Customers (ids) who are primary on a loan with `purpose = 'Construction'`, using `IN`. Return the count of distinct such customers.",
      "SELECT COUNT(*) FROM customer WHERE customer_id IN (SELECT primary_customer_id FROM loan WHERE purpose='Construction')"),
    P(1, "The single largest loan: `loan_id`, `original_amount` for the loan(s) whose amount equals `MAX(original_amount)` (use a subquery, not ORDER BY/LIMIT). Sorted by `loan_id`.",
      "SELECT loan_id, original_amount FROM loan WHERE original_amount = (SELECT MAX(original_amount) FROM loan) ORDER BY 1"),
    P(1, "Products that have never been used on a loan (EXISTS/NOT EXISTS). Return `product_id`, `product_name`; sorted by `product_id`. (May be empty.)",
      "SELECT product_id, product_name FROM dim_product p WHERE NOT EXISTS (SELECT 1 FROM loan l WHERE l.product_id=p.product_id) ORDER BY 1", empty_ok=True),
    P(2, "Loans larger than the average loan of their own `purpose` (correlated). Count them. One number.",
      "SELECT COUNT(*) FROM loan o WHERE original_amount > (SELECT AVG(original_amount) FROM loan i WHERE i.purpose=o.purpose)"),
    P(2, "Derived table: average of the per-customer loan counts. Compute loans per primary customer in a subquery, then average (2 dp). One number.",
      "SELECT ROUND(AVG(n),2) FROM (SELECT primary_customer_id, COUNT(*) AS n FROM loan GROUP BY 1)"),
    P(2, "Brokers whose total original lending is above the average of all brokers' totals. Return `broker_id`, `total` (0dp); sorted by `total` descending then id.",
      """SELECT broker_id, ROUND(t,0) FROM (SELECT broker_id, SUM(original_amount) AS t FROM loan WHERE broker_id IS NOT NULL GROUP BY 1)
WHERE t > (SELECT AVG(t2) FROM (SELECT SUM(original_amount) AS t2 FROM loan WHERE broker_id IS NOT NULL GROUP BY broker_id)) ORDER BY t DESC, 1"""),
    P(2, "Customers who have BOTH a closed and an active loan as primary (two EXISTS). Count them. One number.",
      "SELECT COUNT(*) FROM customer c WHERE EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id AND l.loan_status='Active') AND EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id AND l.loan_status='Closed')"),
    P(2, "The latest origination date for each product: `product_id`, `last_orig` using a correlated subquery in WHERE (or GROUP BY). Return all products with loans; sorted by `product_id`.",
      "SELECT product_id, MAX(origination_date) FROM loan GROUP BY 1 ORDER BY 1"),
    P(2, "Loans whose interest rate at origination is above the average rate for loans originated in the SAME year. Count by year. Return `yr`, `loans_above_avg`; sorted by `yr`.",
      "SELECT year(origination_date) AS yr, COUNT(*) FROM loan o WHERE interest_rate_at_origination_pct > (SELECT AVG(interest_rate_at_origination_pct) FROM loan i WHERE year(i.origination_date)=year(o.origination_date)) GROUP BY 1 ORDER BY 1"),
    P(2, "Applications from customers who ALSO have an approved application earlier in time - repeat customers. Count applications where an earlier application (same `primary_customer_id`, earlier `application_date`) with `decision='Approved'` exists. One number.",
      "SELECT COUNT(*) FROM loan_application a WHERE EXISTS (SELECT 1 FROM loan_application b WHERE b.primary_customer_id=a.primary_customer_id AND b.application_date < a.application_date AND b.decision='Approved')"),
    P(2, "Loans in the top-quartile of original amount (>= the 75th percentile): count them using a scalar subquery `(SELECT QUANTILE_CONT(original_amount,0.75) FROM loan)`. One number.",
      "SELECT COUNT(*) FROM loan WHERE original_amount >= (SELECT QUANTILE_CONT(original_amount,0.75) FROM loan)"),
    P(3, "For each state of property, the % of Active loans (snapshot 2025-12-31) that are in 30+ DPD arrears. Derive per-state numerator and denominator in a subquery. Return `state`, `pct_30plus` (2 dp); sorted by `state`.",
      """SELECT state, ROUND(100.0*n30/n,2) FROM (
 SELECT d.state, COUNT(*) AS n, COUNT(*) FILTER (WHERE s.days_past_due>=30) AS n30
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
 WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1) ORDER BY 1"""),
    P(3, "The second-highest original_amount (distinct value). Use a subquery with MAX and `<`. One number.",
      "SELECT MAX(original_amount) FROM loan WHERE original_amount < (SELECT MAX(original_amount) FROM loan)"),
    P(3, "Customers whose every loan (as primary) is closed - 'ex-customers'. Use `NOT EXISTS` for any non-closed loan AND require at least one loan. Count them. One number.",
      "SELECT COUNT(*) FROM customer c WHERE EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id) AND NOT EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id AND l.loan_status<>'Closed')"),
    P(3, "Branch league: branches whose Active-loan count is above the median branch count. Return `branch_id`, `loans` for those; sorted by `loans` descending then id. (Branch NULL excluded.)",
      """SELECT branch_id, n FROM (SELECT branch_id, COUNT(*) AS n FROM loan WHERE loan_status='Active' AND branch_id IS NOT NULL GROUP BY 1)
WHERE n > (SELECT MEDIAN(n) FROM (SELECT COUNT(*) AS n FROM loan WHERE loan_status='Active' AND branch_id IS NOT NULL GROUP BY branch_id)) ORDER BY n DESC, 1"""),
    P(3, "Loans that were ever in 90+ DPD (any snapshot) but are NOT in arrears now (latest snapshot dpd = 0 and not closed). Count them. One number.",
      """SELECT COUNT(*) FROM loan_monthly_snapshot s WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND s.days_past_due=0
AND EXISTS (SELECT 1 FROM loan_monthly_snapshot h WHERE h.loan_id=s.loan_id AND h.days_past_due>=90)"""),
    P(3, "Scalar subquery in SELECT: for loans 1-8 show `loan_id`, `original_amount`, and the average amount for loans of the same purpose (rounded 0 dp) as `purpose_avg`. Sorted by `loan_id`.",
      "SELECT l.loan_id, l.original_amount, (SELECT ROUND(AVG(i.original_amount),0) FROM loan i WHERE i.purpose=l.purpose) FROM loan l WHERE l.loan_id <= 8 ORDER BY 1"),
    P(3, "Customers who applied but were NEVER approved on any application, yet applied at least 3 times. Count them. One number.",
      "SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application GROUP BY 1 HAVING COUNT(*)>=3 AND COUNT(*) FILTER (WHERE decision='Approved')=0)"),
])
