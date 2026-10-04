# 07 - Advanced joins: anti/semi, self, range, fan-out

`answers/07_joins_advanced/qNN.sql` &nbsp;|&nbsp; check with: `grade 07` or `grade 07 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Beyond the basic join

**Anti-join** - rows in A with NO match in B ("customers who never borrowed"):
```
 SELECT ... FROM A WHERE NOT EXISTS (SELECT 1 FROM B WHERE B.k = A.k)      -- safest
 SELECT ... FROM A LEFT JOIN B ON B.k = A.k WHERE B.k IS NULL             -- also fine
```
**Semi-join** - rows in A that HAVE a match, without duplicating them: `WHERE EXISTS (...)` or `WHERE k IN (SELECT k FROM B)`.

**Self-join** - a table joined to itself under two aliases (staff -> manager, loan -> parent loan):
```
 FROM dim_staff e JOIN dim_staff m ON m.staff_id = e.manager_staff_id
```
**Range (non-equi) join** - match on `BETWEEN`, not `=`: which RBA rate applied on a date? Which policy epoch was an application assessed under?
```
 JOIN ref_serviceability_policy p ON a.application_date >= p.effective_from AND a.application_date <= p.effective_to
```
**Fan-out** - joining 1 row to N rows repeats the 1-side's numbers. Summing a loan amount after joining to `loan_borrower` double-counts joint loans:
```
 loan (1 row, $500k)  --JOIN-->  loan_borrower (2 rows)   => $500k appears twice, SUM = $1m (wrong!)
```
Fix: aggregate the many-side to the loan grain first, or count `DISTINCT`, or join to only one row (the primary).

**Slowly-changing history tables** (`loan_rate_history`, `property_valuation`): "value at date X" = the row where `effective_from <= X < effective_to` (NULL `effective_to` = still current).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Customers who have never been the primary borrower on a loan (anti-join). How many? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Applications that became a loan (semi-join): count of applications with a matching loan. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Staff and their manager: `staff_id`, `full_name`, `manager_name` for staff 1-12 (LEFT JOIN so the top person shows NULL manager). Sorted by `staff_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★★ &nbsp; (core)

Number of direct reports per manager. Return `manager_name`, `reports`; sorted by `reports` descending then name.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **25 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Internal refinance chain: join each child loan to its parent (`parent_loan_id`). Return `child_loan_id`, `parent_loan_id`, `parent_closed_date`, `child_origination_date` for the first 10 children by child id. (Parent should close when the child is created.)

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Which serviceability policy epoch was each application assessed under? Range-join `loan_application.application_date` to `ref_serviceability_policy` and count applications per `policy_id`. Return `policy_id`, `applications`; sorted by `policy_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Fan-out demonstration. Compute (a) the true total `original_amount` across loans and (b) the total after joining `loan` to `loan_borrower` (wrong). Return one row: `true_total`, `fanned_total` both rounded to 0 dp.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★ &nbsp; (core)

Cross-collateral loans: loans with more than one `loan_security` row. Return `loan_id`, `securities` sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **883 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Loans that have NEVER had a hardship arrangement: count by `loan_status`. Return `loan_status`, `loans`; sorted by `loan_status`. (Anti-join.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Which RBA cash rate applied to the bank on 2024-03-15? Range-join date to `ref_rba_cash_rate` using `bank_effective_date` to the next row's effective date. Simplest: return the `cash_rate_pct` of the latest row with `bank_effective_date <= DATE '2024-03-15'`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Interest rate on loan 1 as at 2022-12-31 using `loan_rate_history` (`effective_from <= date` and (`effective_to` is NULL or `effective_to` > date)). Return `loan_id`, `interest_rate_pct` for loans 1-10 that were already originated by that date. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Rate-change history: for loans 1-15 count the rows in `loan_rate_history` whose `change_reason` is `'RBA cash rate pass-through'`. Return `loan_id`, `rate_changes`; sorted by `loan_id`. Loans with none should show 0.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Co-borrower income uplift. For applications with a co-applicant, how many have the co-applicant earning more than the primary? Use `application_applicant` joined to itself on `application_id` (Primary vs Co-applicant) and `income_share_pct`. Return one number: applications where co-applicant `income_share_pct` > primary's.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Application resubmissions. `resubmission_of_application_id` points to an earlier application. For resubmissions, return the previous application's `current_status` and the number of resubmissions per that status. Return `prior_status`, `resubmissions`; sorted by count descending then status.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Anti-join on a pair of keys. Customers whose bureau report exists on an application but who are NOT listed in `application_applicant` for that same application (a referential gap). Count them. (Probably 0; `empty_ok`).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

HPI revaluation join: index the loan's property to 2025-12-31. For loans 1-10 (non-internal) get the property's state through `dim_postcode`, then the `price_index` for that state at `month_end_date` = `last_day(origination_date)` and at `2025-12-31`. Return `loan_id`, `idx_orig`, `idx_now`, `growth_pct` (1dp) = (now/orig-1)*100. Sorted by `loan_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

Join the index table twice with different aliases (`o` for origination, `n` for now).

</details>

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Valuations per property: each property can have several valuation rows. For loans 1-10 list `loan_id` and the count of valuations of the loan's property and the count that are AVM zeros (valuation_amount = 0). Return `loan_id`, `valuations`, `zero_valuations`; sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Cohort pairing: pair each Active loan on loan_id 1-6 with every policy epoch (CROSS JOIN) and show whether the loan's `origination_date` fell within that epoch. Return `loan_id`, `policy_id`, `in_epoch` (boolean); sorted by `loan_id`, `policy_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Staff authority breach: loans where the assessor's `lending_authority_limit` is below the loan's `original_amount`. (Policy exceptions should explain these.) Return the count of such loans. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2019 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2020 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2021 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2022 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2023 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2024 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★ &nbsp; (core)

Anti-join: customers who lodged an application in 2025 but have NEVER had a loan as primary. Count them. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★ &nbsp; (core)

Semi-join: how many distinct customers with a `'Purchase - Owner Occupied'` loan (primary) have also been in a hardship arrangement on any of their loans? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★ &nbsp; (core)

Semi-join: how many distinct customers with a `'Purchase - Investment'` loan (primary) have also been in a hardship arrangement on any of their loans? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★ &nbsp; (core)

Semi-join: how many distinct customers with a `'Refinance'` loan (primary) have also been in a hardship arrangement on any of their loans? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★ &nbsp; (core)

Semi-join: how many distinct customers with a `'Equity Release / Top-up'` loan (primary) have also been in a hardship arrangement on any of their loans? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★ &nbsp; (core)

Semi-join: how many distinct customers with a `'Construction'` loan (primary) have also been in a hardship arrangement on any of their loans? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★ &nbsp; (core)

Range join: `'Broker'`-channel applications per serviceability `policy_id` (match `application_date` to the policy's effective window). `policy_id`, `applications`; sorted by policy.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Range join: `'Branch'`-channel applications per serviceability `policy_id` (match `application_date` to the policy's effective window). `policy_id`, `applications`; sorted by policy.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★ &nbsp; (core)

Range join: `'Digital'`-channel applications per serviceability `policy_id` (match `application_date` to the policy's effective window). `policy_id`, `applications`; sorted by policy.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Range join: `'Mobile Lender'`-channel applications per serviceability `policy_id` (match `application_date` to the policy's effective window). `policy_id`, `applications`; sorted by policy.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Fan-out: for `'Purchase - Owner Occupied'` loans, the true total `original_amount` and the total after joining to `loan_borrower` (double-counts joint loans), both 0 dp. `true_total`, `fanned_total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★★ &nbsp; (challenge)

Fan-out: for `'Purchase - Investment'` loans, the true total `original_amount` and the total after joining to `loan_borrower` (double-counts joint loans), both 0 dp. `true_total`, `fanned_total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★★ &nbsp; (challenge)

Fan-out: for `'Refinance'` loans, the true total `original_amount` and the total after joining to `loan_borrower` (double-counts joint loans), both 0 dp. `true_total`, `fanned_total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★★ &nbsp; (challenge)

Fan-out: for `'Equity Release / Top-up'` loans, the true total `original_amount` and the total after joining to `loan_borrower` (double-counts joint loans), both 0 dp. `true_total`, `fanned_total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★★ &nbsp; (challenge)

Fan-out: for `'Construction'` loans, the true total `original_amount` and the total after joining to `loan_borrower` (double-counts joint loans), both 0 dp. `true_total`, `fanned_total`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★★ &nbsp; (challenge)

Point-in-time: the average interest rate (3 dp) in force across all loans on 2020-06-30, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★★★ &nbsp; (challenge)

Point-in-time: the average interest rate (3 dp) in force across all loans on 2021-06-30, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★★ &nbsp; (challenge)

Point-in-time: the average interest rate (3 dp) in force across all loans on 2022-06-30, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★★ &nbsp; (challenge)

Point-in-time: the average interest rate (3 dp) in force across all loans on 2023-06-30, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★★ &nbsp; (challenge)

Point-in-time: the average interest rate (3 dp) in force across all loans on 2024-06-30, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q46 &nbsp; ★★★ &nbsp; (challenge)

Point-in-time: the average interest rate (3 dp) in force across all loans on 2025-06-30, from `loan_rate_history` (`effective_from <= date` and `effective_to` NULL or after the date; ignore fractional keyed rates below 1). Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q47 &nbsp; ★★ &nbsp; (core)

House price index for `'NSW'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q48 &nbsp; ★★ &nbsp; (core)

House price index for `'VIC'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q49 &nbsp; ★★ &nbsp; (core)

House price index for `'QLD'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q50 &nbsp; ★★ &nbsp; (core)

House price index for `'SA'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q51 &nbsp; ★★ &nbsp; (core)

House price index for `'WA'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q52 &nbsp; ★★ &nbsp; (core)

House price index for `'TAS'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q53 &nbsp; ★★ &nbsp; (core)

House price index for `'NT'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q54 &nbsp; ★★ &nbsp; (core)

House price index for `'ACT'` at 2020-12-31 and 2025-12-31 side by side (join `ref_property_price_index` to itself) and growth % (1 dp). `idx_2020`, `idx_2025`, `growth_pct`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q55 &nbsp; ★★ &nbsp; (core)

Self-join: staff in the `'Broker Credit'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q56 &nbsp; ★★ &nbsp; (core)

Self-join: staff in the `'Retail Credit'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q57 &nbsp; ★★ &nbsp; (core)

Self-join: staff in the `'Collections'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q58 &nbsp; ★★ &nbsp; (core)

Self-join: staff in the `'Complex Lending'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q59 &nbsp; ★★ &nbsp; (core)

Self-join: staff in the `'Credit Risk'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q60 &nbsp; ★★ &nbsp; (core)

Self-join: staff in the `'Hardship'` team with their manager's name and the manager's team. `staff_id`, `full_name`, `manager_name`, `manager_team`; sorted by `staff_id`; first 10 only.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.
