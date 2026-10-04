# 03 - NULLs, COALESCE, NULLIF, three-valued logic

`answers/03_nulls/qNN.sql` &nbsp;|&nbsp; check with: `grade 03` or `grade 03 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## NULL = "unknown / not applicable" - not zero, not empty text

```
   5 + NULL      -> NULL          NULL = NULL    -> NULL (not TRUE!)
   NULL > 3      -> NULL          NULL <> 'x'    -> NULL
   TRUE AND NULL -> NULL          TRUE OR NULL   -> TRUE
```

`WHERE` keeps a row only when the test is **TRUE**. NULL is not TRUE, so those rows silently vanish.

```
  decision column:  Approved | Declined | NULL | Approved | NULL
  WHERE decision <> 'Approved'      keeps only: Declined          (NULLs vanish!)
  WHERE decision IS DISTINCT FROM 'Approved'   keeps: Declined, NULL, NULL
```

### Toolbox
| Need | Write |
|---|---|
| test missing | `x IS NULL`, `x IS NOT NULL` |
| default value | `COALESCE(x, 0)` (first non-NULL of the list) |
| turn a value INTO null | `NULLIF(x, 0)` (handy to avoid divide-by-zero) |
| NULL-safe compare | `a IS NOT DISTINCT FROM b` |
| aggregate behaviour | `COUNT(*)` counts rows, `COUNT(x)` counts non-NULL, `SUM/AVG` skip NULLs |
| sorting | `ORDER BY x NULLS FIRST / NULLS LAST` |
| `NOT IN (subquery)` | returns **nothing** if the subquery contains any NULL - use `NOT EXISTS` |

Credit-risk reality: NULL bureau score = thin file, NULL `branch_id` = no branch involved, NULL `closed_date` = still open. Each means something different - always ask *why* it is NULL.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

How many customers have no `date_of_birth` recorded? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

How many loans have a NULL `branch_id`? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Return one row with two numbers: the count of ALL rows in `credit_bureau_report` and the count of rows with a non-NULL `bureau_score`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★ &nbsp; (warm-up)

How many loans are still open, using the fact that `closed_date` is NULL for open loans? (This should equal active + in-recovery loans.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q05 &nbsp; ★ &nbsp; (warm-up)

For loans 1 to 15, show `loan_id` and `fixed_rate_expiry_date`, replacing NULL with the date 9999-12-31. Sort by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★ &nbsp; (warm-up)

Applications with no decision yet or no final decision recorded: count where `decision IS NULL`, grouped by `current_status`. Return `current_status`, `n`, sorted by `current_status`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

The classic trap. Return one row with two numbers: (a) how many applications have `decision <> 'Approved'`, (b) how many have `decision IS DISTINCT FROM 'Approved'`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★ &nbsp; (core)

Broker-channel applications that are missing a broker (`broker_id` NULL): this is a data-quality problem. Return `application_id`, `application_date`, sorted by `application_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **245 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Average bureau score: return two numbers - the plain `AVG(bureau_score)` rounded to 1 dp, and the average if NULL scores were wrongly treated as 0 (`AVG(COALESCE(bureau_score,0))`) rounded to 1 dp. Which would mislead a credit committee?

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

For each `income_type` return how many income lines have a NULL `verified_annual_amount` (unverified). Return `income_type`, `unverified_lines`, sorted by `unverified_lines` descending then `income_type`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Income used for assessment: `COALESCE(verified_annual_amount, declared_annual_amount)`. Return the total of that across all income lines, rounded to 0 dp, as `assessed_income_total`.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★ &nbsp; (core)

Safe division. For loan 1..30 compute `original_amount / NULLIF(io_period_months,0)` rounded to 2 dp (monthly principal-like figure). Return `loan_id`, value; sorted by `loan_id`. Loans with no IO period will show NULL rather than an error.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

Count loans by `branch_id`, but show NULL branches as the label `'No branch'`. Return `branch_label` (text), `loans`; sorted by `loans` descending then `branch_label`. Hint: cast the id to text before COALESCE.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **61 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

`COALESCE(CAST(branch_id AS VARCHAR), 'No branch')`

</details>

### Q14 &nbsp; ★★ &nbsp; (core)

Loans where `branch_id` is NULL, split by `channel`. Return `channel`, `loans` sorted by `channel`. (What does this tell you about whether NULL is a data error here?)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

Application-level pass rate. For each `channel`, compute the % of applications with `decision = 'Approved'` out of ALL applications (rounded to 1 dp). Return `channel`, `approved_pct`; sorted by `channel`. Careful: `AVG(CASE ... )` vs `COUNT(decision)`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

Same question but the denominator is only applications that actually reached a decision (`decision IS NOT NULL`). Return `channel`, `approval_rate_pct` (1dp); sorted by `channel`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

NULL-safe join key. `loan.application_id` is NULL for internal-refinance child loans. How many loans have a NULL `application_id`, and how many of those have `purpose = 'Internal Refinance'`? Return two numbers.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

`NOT IN` trap. Count applications that were NOT lodged via a `'Terminated'` broker (`dim_broker.status`). Applications with a NULL `broker_id` must be counted (they have no terminated broker). Return one number. Write it with `NOT EXISTS`; then try `NOT IN` on `broker_id` and see why it breaks.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Sort with NULLs last. List the 10 loans with the earliest `fixed_rate_expiry_date` that is NOT NULL: return `loan_id`, `fixed_rate_expiry_date`; ties by `loan_id`. Then think about what `ORDER BY ... DESC` would do with NULLs.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Customers with a missing DOB: how many of them have also been flagged as duplicates? Duplicates have the same `first_name`, `last_name` (case-insensitive, trimmed) and `postcode`. Return one number: the count of NULL-DOB customers who share lowercase/trimmed name+postcode with at least one other customer.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Build a single 'bureau quality' label with CASE: `'Thin file'` when `bureau_score IS NULL`, `'Adverse'` when `bankruptcy_flag` or `court_judgements > 0`, `'Weak'` when score < 600, `'Fair'` when 600-749, else `'Strong'`. Return `quality`, `reports` ordered by `reports` descending, then `quality`. Order of the CASE branches matters.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `customer` have a NULL `date_of_birth`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `branch_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `broker_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `fixed_rate_expiry_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `closed_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `closure_reason`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `application_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `parent_loan_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_application` have a NULL `broker_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_application` have a NULL `decision`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_application` have a NULL `decline_reason_code`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_application` have a NULL `decision_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_application` have a NULL `withdrawn_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_application` have a NULL `resubmission_of_application_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `credit_bureau_report` have a NULL `bureau_score`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `applicant_income` have a NULL `verified_annual_amount`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `collections_activity` have a NULL `promise_amount`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `hardship_arrangement` have a NULL `end_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `complaint` have a NULL `resolved_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `dim_staff` have a NULL `termination_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `dim_staff` have a NULL `manager_staff_id`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `dim_branch` have a NULL `closed_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan` have a NULL `io_expiry_date`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★ &nbsp; (warm-up)

NULL profile: what percentage (2 dp) of rows in `loan_payment` have a NULL `failure_reason`? Return one number. (Think about WHY they are NULL.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q46 &nbsp; ★★ &nbsp; (core)

For `'Broker'` loans: how many have a NULL `branch_id` and how many have a NULL `broker_id`? Return `null_branch`, `null_broker`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q47 &nbsp; ★★ &nbsp; (core)

For `'Branch'` loans: how many have a NULL `branch_id` and how many have a NULL `broker_id`? Return `null_branch`, `null_broker`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q48 &nbsp; ★★ &nbsp; (core)

For `'Digital'` loans: how many have a NULL `branch_id` and how many have a NULL `broker_id`? Return `null_branch`, `null_broker`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q49 &nbsp; ★★ &nbsp; (core)

For `'Mobile Lender'` loans: how many have a NULL `branch_id` and how many have a NULL `broker_id`? Return `null_branch`, `null_broker`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q50 &nbsp; ★★ &nbsp; (core)

For `'Purchase - Owner Occupied'` loans: the average `io_period_months` with NULLs treated as 0 (`COALESCE`), and the average ignoring NULLs - both 2 dp. Return `avg_coalesced`, `avg_plain`. (If both are equal, no NULLs exist - say why.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q51 &nbsp; ★★ &nbsp; (core)

For `'Purchase - Investment'` loans: the average `io_period_months` with NULLs treated as 0 (`COALESCE`), and the average ignoring NULLs - both 2 dp. Return `avg_coalesced`, `avg_plain`. (If both are equal, no NULLs exist - say why.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q52 &nbsp; ★★ &nbsp; (core)

For `'Refinance'` loans: the average `io_period_months` with NULLs treated as 0 (`COALESCE`), and the average ignoring NULLs - both 2 dp. Return `avg_coalesced`, `avg_plain`. (If both are equal, no NULLs exist - say why.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q53 &nbsp; ★★ &nbsp; (core)

For `'Equity Release / Top-up'` loans: the average `io_period_months` with NULLs treated as 0 (`COALESCE`), and the average ignoring NULLs - both 2 dp. Return `avg_coalesced`, `avg_plain`. (If both are equal, no NULLs exist - say why.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q54 &nbsp; ★★ &nbsp; (core)

For `'Construction'` loans: the average `io_period_months` with NULLs treated as 0 (`COALESCE`), and the average ignoring NULLs - both 2 dp. Return `avg_coalesced`, `avg_plain`. (If both are equal, no NULLs exist - say why.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q55 &nbsp; ★★★ &nbsp; (challenge)

`COUNT(*)` vs `COUNT(col)`: for each `decision` status in `loan_application` (including NULL shown as `'(none)'`) return `decision_label`, `apps`, `with_decline_code` (`COUNT(decline_reason_code)`). Sorted by `decision_label`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q56 &nbsp; ★★★ &nbsp; (challenge)

`IS NOT DISTINCT FROM`: count loans whose `branch_id` IS NOT DISTINCT FROM the branch on the originating application (join on `application_id`). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q57 &nbsp; ★★★ &nbsp; (challenge)

NULLS LAST: the 5 customers with the latest `date_of_birth` (youngest), ties by `customer_id`, where NULL DOBs must NOT appear first. Return `customer_id`, `date_of_birth`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q58 &nbsp; ★★★ &nbsp; (challenge)

Average of averages trap: average `bureau_score` across ALL reports (2 dp) vs the average of per-`enquiries_last_12m` averages (2 dp). Return `overall_avg`, `avg_of_avgs`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q59 &nbsp; ★★★ &nbsp; (challenge)

Coalesce chain: for loans 1-10 show the first non-NULL of `closed_date`, `fixed_rate_expiry_date`, `maturity_date` as `key_date`. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.
