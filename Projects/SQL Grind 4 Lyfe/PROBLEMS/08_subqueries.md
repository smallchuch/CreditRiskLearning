# 08 - Subqueries: scalar, IN, EXISTS, correlated, derived tables

`answers/08_subqueries/qNN.sql` &nbsp;|&nbsp; check with: `grade 08` or `grade 08 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans with an original amount above the average original amount. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Customers (ids) who are primary on a loan with `purpose = 'Construction'`, using `IN`. Return the count of distinct such customers.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

The single largest loan: `loan_id`, `original_amount` for the loan(s) whose amount equals `MAX(original_amount)` (use a subquery, not ORDER BY/LIMIT). Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **14 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★ &nbsp; (warm-up)

Products that have never been used on a loan (EXISTS/NOT EXISTS). Return `product_id`, `product_name`; sorted by `product_id`. (May be empty.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **0 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Loans larger than the average loan of their own `purpose` (correlated). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Derived table: average of the per-customer loan counts. Compute loans per primary customer in a subquery, then average (2 dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

Brokers whose total original lending is above the average of all brokers' totals. Return `broker_id`, `total` (0dp); sorted by `total` descending then id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **85 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Customers who have BOTH a closed and an active loan as primary (two EXISTS). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★ &nbsp; (core)

The latest origination date for each product: `product_id`, `last_orig` using a correlated subquery in WHERE (or GROUP BY). Return all products with loans; sorted by `product_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Loans whose interest rate at origination is above the average rate for loans originated in the SAME year. Count by year. Return `yr`, `loans_above_avg`; sorted by `yr`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Applications from customers who ALSO have an approved application earlier in time - repeat customers. Count applications where an earlier application (same `primary_customer_id`, earlier `application_date`) with `decision='Approved'` exists. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★ &nbsp; (core)

Loans in the top-quartile of original amount (>= the 75th percentile): count them using a scalar subquery `(SELECT QUANTILE_CONT(original_amount,0.75) FROM loan)`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

For each state of property, the % of Active loans (snapshot 2025-12-31) that are in 30+ DPD arrears. Derive per-state numerator and denominator in a subquery. Return `state`, `pct_30plus` (2 dp); sorted by `state`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

The second-highest original_amount (distinct value). Use a subquery with MAX and `<`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Customers whose every loan (as primary) is closed - 'ex-customers'. Use `NOT EXISTS` for any non-closed loan AND require at least one loan. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Branch league: branches whose Active-loan count is above the median branch count. Return `branch_id`, `loans` for those; sorted by `loans` descending then id. (Branch NULL excluded.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Loans that were ever in 90+ DPD (any snapshot) but are NOT in arrears now (latest snapshot dpd = 0 and not closed). Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Scalar subquery in SELECT: for loans 1-8 show `loan_id`, `original_amount`, and the average amount for loans of the same purpose (rounded 0 dp) as `purpose_avg`. Sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Customers who applied but were NEVER approved on any application, yet applied at least 3 times. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Loans with purpose `'Purchase - Owner Occupied'` bigger than the average `'Purchase - Owner Occupied'` loan: count them. (Scalar subquery.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Loans with purpose `'Purchase - Investment'` bigger than the average `'Purchase - Investment'` loan: count them. (Scalar subquery.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Loans with purpose `'Refinance'` bigger than the average `'Refinance'` loan: count them. (Scalar subquery.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Loans with purpose `'Equity Release / Top-up'` bigger than the average `'Equity Release / Top-up'` loan: count them. (Scalar subquery.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Loans with purpose `'Construction'` bigger than the average `'Construction'` loan: count them. (Scalar subquery.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Loans originated in 2019 with an original amount above the average for 2019 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Loans originated in 2020 with an original amount above the average for 2020 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Loans originated in 2021 with an original amount above the average for 2021 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Loans originated in 2022 with an original amount above the average for 2022 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Loans originated in 2023 with an original amount above the average for 2023 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Loans originated in 2024 with an original amount above the average for 2024 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

Loans originated in 2025 with an original amount above the average for 2025 loans. Count them. (Subquery filters to the same year.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'NSW'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'VIC'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'QLD'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'SA'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'WA'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'TAS'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'NT'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★ &nbsp; (core)

`IN` subquery: customers whose `state` is exactly `'ACT'` and who are primary on at least one loan. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★ &nbsp; (core)

`EXISTS`: distinct primary customers with a loan that had a `'COVID-19 repayment deferral'` hardship arrangement. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★ &nbsp; (core)

`EXISTS`: distinct primary customers with a loan that had a `'Reduced repayments'` hardship arrangement. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★ &nbsp; (core)

`EXISTS`: distinct primary customers with a loan that had a `'Repayment deferral'` hardship arrangement. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★ &nbsp; (core)

`EXISTS`: distinct primary customers with a loan that had a `'Interest-only period'` hardship arrangement. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★ &nbsp; (core)

`EXISTS`: distinct primary customers with a loan that had a `'Term extension'` hardship arrangement. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★ &nbsp; (core)

`EXISTS`: distinct primary customers with a loan that had a `'Arrears capitalisation'` hardship arrangement. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q46 &nbsp; ★★★ &nbsp; (challenge)

Derived table: for `'Broker'` loans, the average number of loans per primary customer (2 dp) - count per customer in a subquery, then average. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q47 &nbsp; ★★★ &nbsp; (challenge)

Derived table: for `'Branch'` loans, the average number of loans per primary customer (2 dp) - count per customer in a subquery, then average. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q48 &nbsp; ★★★ &nbsp; (challenge)

Derived table: for `'Digital'` loans, the average number of loans per primary customer (2 dp) - count per customer in a subquery, then average. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q49 &nbsp; ★★★ &nbsp; (challenge)

Derived table: for `'Mobile Lender'` loans, the average number of loans per primary customer (2 dp) - count per customer in a subquery, then average. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q50 &nbsp; ★★★ &nbsp; (challenge)

Branches in `'NSW'` that originated MORE loans than the average branch (average over all branches that originated any loan). `branch_id`, `loans`; sorted by loans descending then id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q51 &nbsp; ★★★ &nbsp; (challenge)

Branches in `'VIC'` that originated MORE loans than the average branch (average over all branches that originated any loan). `branch_id`, `loans`; sorted by loans descending then id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q52 &nbsp; ★★★ &nbsp; (challenge)

Branches in `'QLD'` that originated MORE loans than the average branch (average over all branches that originated any loan). `branch_id`, `loans`; sorted by loans descending then id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q53 &nbsp; ★★★ &nbsp; (challenge)

Branches in `'SA'` that originated MORE loans than the average branch (average over all branches that originated any loan). `branch_id`, `loans`; sorted by loans descending then id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **13 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q54 &nbsp; ★★★ &nbsp; (challenge)

Branches in `'WA'` that originated MORE loans than the average branch (average over all branches that originated any loan). `branch_id`, `loans`; sorted by loans descending then id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **0 row(s)** &nbsp;|&nbsp; Sort the output as described.
