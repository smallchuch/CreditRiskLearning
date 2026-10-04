# 06 - JOINs: inner, left, multiple tables

`answers/06_joins_basic/qNN.sql` &nbsp;|&nbsp; check with: `grade 06` or `grade 06 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

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

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Loans with their product name: `loan_id`, `product_name` for loans 1-10, sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Number of loans per `product_name`. Return `product_name`, `loans`; sorted by `loans` descending then `product_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Loans 1-10 with the primary borrower's surname: `loan_id`, `last_name`. Join `loan` to `customer` on `primary_customer_id`. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★ &nbsp; (warm-up)

Loans 1-10 and the branch name that wrote them (`dim_branch`). Use a LEFT JOIN so loans with no branch still appear (branch_name NULL). Return `loan_id`, `branch_name`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★ &nbsp; (warm-up)

Count of loans per state of the property: join `loan` -> `property` -> `dim_postcode`. Return `state`, `loans`; sorted by `state`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Co-borrowers: number of loans with exactly 2 borrowers on `loan_borrower`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q07 &nbsp; ★★ &nbsp; (core)

Loans with the broker firm and aggregator for Broker-channel loans 1-200 that have a broker: `loan_id`, `firm_name`, `aggregator`; sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **91 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Total original amount by aggregator. Return `aggregator`, `total_amount` (0 dp); sorted by `total_amount` descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

The assessor behind each loan: count loans by assessor `team` (join `dim_staff` on `assessor_staff_id`). Return `team`, `loans`; sorted by `loans` descending then `team`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Loan-level LVR cross-check: join `loan` to `loan_application` on `application_id`. For loans 1-10 return `loan_id`, `requested_amount`, `original_amount` (the loan may be resized). Sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Declined applications with the reason description: `application_id`, `reason_description` for applications 1-60 with `decision='Declined'`. Join `ref_decline_reason` on code. Sorted by `application_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **17 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

Decline reasons by category: `reason_category`, `declined_apps`; sorted by count descending then category.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

Arrears bucket labels. Using `ref_arrears_bucket` joined on `days_past_due BETWEEN dpd_from AND COALESCE(dpd_to, 99999)` count non-closed loans at 2025-12-31 per `bucket_name`. Return `bucket_name`, `loans`; sorted by `bucket_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★ &nbsp; (core)

Hardship by team: join `hardship_arrangement` to `loan` and count arrangements per loan `purpose`. Return `purpose`, `arrangements`; sorted by `arrangements` descending then `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

Complaints with their loan product: count complaints per `product_name` (some complaints have no loan - drop them). Return `product_name`, `complaints`; sorted by `complaints` descending then `product_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

LEFT JOIN trap. Customers 1-30 with the number of loans they are primary on - customers with no loan must show 0. Return `customer_id`, `loans`; sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

`COUNT(l.loan_id)` counts matches only; `COUNT(*)` would give 1 for the no-match customers.

</details>

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Valuation at origination vs now: for loans 1-10 return `loan_id`, `security_value_at_origination`, and the latest `valuation_amount` for the loan's property from `property_valuation` with `valuation_date <= 2025-12-31` that is > 0 (AVM zeros are bad data). Sorted by `loan_id`. Use a subquery or join on MAX(valuation_date).

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Join through the application: for approved-and-settled applications in 2025 (`current_status='Settled'`, `application_date` in 2025) show average bureau score (join `credit_bureau_report` on application_id and customer = primary customer) per `channel`, 0 dp. Return `channel`, `avg_score`; sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Income per application: `application_income` = SUM of `COALESCE(verified, declared)` across `applicant_income`. Return average per `channel` (0 dp) for applications in 2025. Return `channel`, `avg_income`; sorted by `channel`. (Watch the grain: sum incomes per application first, then average.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Month-end calendar join: for each month-end `snapshot_date` in 2025 list `snapshot_date` and its `day_name` from `dim_date` (distinct dates only). Sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Brokers who wrote no loans at all (LEFT JOIN, filter NULL on the right). Return `broker_id`, `firm_name`, sorted by `broker_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★ &nbsp; (warm-up)

For `'Purchase - Owner Occupied'` loans: the 3 `product_name`s with the most loans. `product_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★ &nbsp; (warm-up)

For `'Purchase - Investment'` loans: the 3 `product_name`s with the most loans. `product_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★ &nbsp; (warm-up)

For `'Refinance'` loans: the 3 `product_name`s with the most loans. `product_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★ &nbsp; (warm-up)

For `'Equity Release / Top-up'` loans: the 3 `product_name`s with the most loans. `product_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★ &nbsp; (warm-up)

For `'Construction'` loans: the 3 `product_name`s with the most loans. `product_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★★ &nbsp; (core)

Loans written via `'Broker'` by property state: `state`, `loans`; sorted by `state`. (Join loan -> property -> dim_postcode.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★★ &nbsp; (core)

Loans written via `'Branch'` by property state: `state`, `loans`; sorted by `state`. (Join loan -> property -> dim_postcode.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★ &nbsp; (core)

Loans written via `'Digital'` by property state: `state`, `loans`; sorted by `state`. (Join loan -> property -> dim_postcode.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

Loans written via `'Mobile Lender'` by property state: `state`, `loans`; sorted by `state`. (Join loan -> property -> dim_postcode.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

The 5 branches in `'NSW'` that originated the most loans: `branch_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

The 5 branches in `'VIC'` that originated the most loans: `branch_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

The 5 branches in `'QLD'` that originated the most loans: `branch_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

The 5 branches in `'SA'` that originated the most loans: `branch_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

The 5 branches in `'WA'` that originated the most loans: `branch_name`, `loans`; most first, ties by name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2019: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2020: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2021: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2022: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2023: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2024: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★ &nbsp; (core)

Settled applications lodged in 2025: average primary-applicant bureau score by `channel` (0 dp). `channel`, `avg_score`; sorted by channel.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q43 &nbsp; ★★ &nbsp; (core)

Loans originated in 2019 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q44 &nbsp; ★★ &nbsp; (core)

Loans originated in 2020 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q45 &nbsp; ★★ &nbsp; (core)

Loans originated in 2021 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q46 &nbsp; ★★ &nbsp; (core)

Loans originated in 2022 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q47 &nbsp; ★★ &nbsp; (core)

Loans originated in 2023 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q48 &nbsp; ★★ &nbsp; (core)

Loans originated in 2024 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q49 &nbsp; ★★ &nbsp; (core)

Loans originated in 2025 by assessor `team` (join `dim_staff`). `team`, `loans`; sorted by team.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q50 &nbsp; ★★★ &nbsp; (challenge)

LEFT JOIN keeps all 15 products: loans per product originated in 2019, with 0 for products with none. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q51 &nbsp; ★★★ &nbsp; (challenge)

LEFT JOIN keeps all 15 products: loans per product originated in 2022, with 0 for products with none. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q52 &nbsp; ★★★ &nbsp; (challenge)

LEFT JOIN keeps all 15 products: loans per product originated in 2025, with 0 for products with none. `product_id`, `loans`; sorted by product_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q53 &nbsp; ★★ &nbsp; (core)

Hardship type `'COVID-19 repayment deferral'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q54 &nbsp; ★★ &nbsp; (core)

Hardship type `'Reduced repayments'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q55 &nbsp; ★★ &nbsp; (core)

Hardship type `'Repayment deferral'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q56 &nbsp; ★★ &nbsp; (core)

Hardship type `'Interest-only period'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q57 &nbsp; ★★ &nbsp; (core)

Hardship type `'Term extension'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q58 &nbsp; ★★ &nbsp; (core)

Hardship type `'Arrears capitalisation'`: arrangements by loan `purpose` (join `loan`). `purpose`, `arrangements`; sorted by purpose.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q59 &nbsp; ★★★ &nbsp; (challenge)

Applications to loans to customers: for loans 1-10 return `loan_id`, the primary customer's `segment`, and the product `occupancy`. Three joins. Sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q60 &nbsp; ★★★ &nbsp; (challenge)

Join four tables: for 2025 settled loans, total original amount by customer `segment` and property `state`; `segment`, `state`, `amount` (0 dp). Sorted by segment, state.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q61 &nbsp; ★★★ &nbsp; (challenge)

Complaints with their branch: count complaints (with a loan) by branch region (loan -> branch; drop loans without a branch). `region`, `complaints`; sorted by complaints descending then region.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **25 row(s)** &nbsp;|&nbsp; Sort the output as described.
