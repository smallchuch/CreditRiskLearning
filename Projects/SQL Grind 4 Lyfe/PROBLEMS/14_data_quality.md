# 14 - Data quality: duplicates, orphans, ranges, gaps and islands

`answers/14_data_quality/qNN.sql` &nbsp;|&nbsp; check with: `grade 14` or `grade 14 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Data quality: the part of the job nobody puts in the tutorial

Real bank data lies. This database has *deliberately planted* problems (see `DATA_QUIRKS_SPOILERS.md` once you have given up - not before!).
A senior analyst's reflexes:

```
 1. Grain check      SELECT key, COUNT(*) FROM t GROUP BY key HAVING COUNT(*) > 1      -- duplicates?
 2. Orphan check     child LEFT JOIN parent ... WHERE parent.key IS NULL                -- broken keys?
 3. Null profile     COUNT(*) vs COUNT(col)                                             -- how complete?
 4. Range check      MIN / MAX / values outside the plausible range                     -- units? zeros?
 5. Consistency      two columns that must agree (dates in order, status vs balance)    -- logic checks
 6. Format check     LENGTH, trim/case variants, odd prefixes                           -- messy text
 7. Reconcile        total in table A = total in table B?                               -- completeness
```

### Gaps and islands
Find missing months (gaps) or unbroken runs (islands) in a sequence:
```
 value - ROW_NUMBER() OVER (ORDER BY value)   is constant inside an island
```
e.g. consecutive months in arrears: `month_index - ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY month_index)`.

Always write down the check, the count it returned, and what you'd do about it. In an interview, *say what you'd check first*.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Duplicate keys test: is `loan_id` unique on `loan`? Return the number of `loan_id` values that appear more than once (0 expected). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Orphan check: loans whose `product_id` is not in `dim_product`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Range check: loans with `lvr_at_origination_pct` outside 0-100 (a loan can't be below 0; above 100 might happen with capitalised costs - count both ways). Return two numbers: below 0, above 100.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★ &nbsp; (warm-up)

Valuation zeros: how many rows in `property_valuation` have `valuation_amount = 0`, grouped by `valuation_type`? Return `valuation_type`, `zero_rows`; sorted by type, only types with at least one zero.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Duplicate customers by normalised name + DOB: groups of rows with the same `LOWER(TRIM(first_name))`, `LOWER(TRIM(last_name))` and `date_of_birth` (non-null). Return the number of duplicate GROUPS. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Messy state values: list every distinct raw `state` value that is NOT one of the 8 clean codes ('NSW','VIC','QLD','SA','WA','TAS','NT','ACT'). Return `state`, `n`; sorted by `n` descending then `state`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **24 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Mobile formats: classify `mobile` as `'04xxxxxxxx'` (starts with `04` and is 10 chars), `'+61 prefix'` (starts with `+61`), or `'other'`; NULL mobile as `'missing'`. Return `format`, `customers`; sorted by `format`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q08 &nbsp; ★★ &nbsp; (core)

Email case: how many customers have an email that is not entirely lowercase (`email <> LOWER(email)`)? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★ &nbsp; (core)

Date logic: loans with `closed_date < origination_date`. Count. (Expect 0.) One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★ &nbsp; (core)

Status vs date consistency: loans with `loan_status = 'Closed'` but NULL `closed_date`, and loans with `loan_status <> 'Closed'` but a non-NULL `closed_date`. Two numbers.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★ &nbsp; (core)

Rates keyed as fractions: in `loan_rate_history`, interest rates below 1 are probably keyed as decimals (0.0629 instead of 6.29). Count rows with `interest_rate_pct < 1`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★ &nbsp; (core)

Application status duplicates: how many (application_id, status) pairs appear more than once in `application_status_history`? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★ &nbsp; (core)

Missing broker on broker-channel applications: count and percentage of Broker-channel applications with NULL `broker_id` (percentage 2dp). Two numbers.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★★ &nbsp; (challenge)

Missing monthly snapshots (gaps): for each loan the expected number of snapshot rows equals `months on book + 1` through its last snapshot. Count loans where the number of snapshot rows differs from `MAX(months_on_book) + 1`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★★ &nbsp; (challenge)

Find the actual missing snapshot months: for loans 1-5000, list `loan_id` and the `months_on_book` values missing between 0 and the loan's max. Use a generate_series/unnest spine. Return `loan_id`, `missing_mob`; sorted by both. (Few rows.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **668 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★★ &nbsp; (challenge)

Islands: for loan 1..N, consecutive-month arrears runs. Using gaps-and-islands on `loan_monthly_snapshot` (non-closed rows with `days_past_due >= 30`), find the longest consecutive run of 30+ DPD snapshot months for any loan. One number: `max_run`. Hint: `months_on_book - ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY months_on_book)` is constant within an island.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★★ &nbsp; (challenge)

Referential integrity across tables: loan_ids in `loan_monthly_snapshot`, `loan_rate_history`, `ecl_provision_quarterly`, `loan_payment`, `hardship_arrangement`, `collections_activity`, `loan_loss` that do not exist in `loan`. Return `tbl`, `orphans` for each; sorted by `tbl`. (All expected 0.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q18 &nbsp; ★★★ &nbsp; (challenge)

Reconcile balances: sum of `closing_balance` at 2025-12-31 for non-closed loans from the snapshot table vs sum of `ead` in `ecl_provision_quarterly` at the same date. Return `snapshot_balance`, `ecl_ead`, `difference` (0dp each). Are they the same population?

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Impossible values: snapshot rows where `days_past_due > 0` but `arrears_amount = 0` and `hardship_flag` is false. Count. One number. (The generator says this should be 0.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Outlier hunt using the IQR rule on `original_amount`: count loans above `Q3 + 1.5*(Q3-Q1)`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Staleness: AVM valuations date. For each property that has at least one valuation, the age in days of its newest valuation as at 2025-12-31 - how many properties have their newest valuation older than 2 years (730 days)? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★★ &nbsp; (challenge)

Unverified income share: per `income_type`, % of lines with NULL `verified_annual_amount` (1dp). Return `income_type`, `unverified_pct`; sorted by pct descending then type.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `customer_id` appear more than once in `customer`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `loan_id` appear more than once in `loan`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `application_id` appear more than once in `loan_application`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `property_id` appear more than once in `property`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `broker_id` appear more than once in `dim_broker`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `staff_id` appear more than once in `dim_staff`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `branch_id` appear more than once in `dim_branch`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `report_id` appear more than once in `credit_bureau_report`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `income_id` appear more than once in `applicant_income`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `liability_id` appear more than once in `applicant_liability`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `event_id` appear more than once in `application_status_history`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `event_id` appear more than once in `loan_event`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `rate_history_id` appear more than once in `loan_rate_history`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `payment_id` appear more than once in `loan_payment`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `hardship_id` appear more than once in `hardship_arrangement`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `activity_id` appear more than once in `collections_activity`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `complaint_id` appear more than once in `complaint`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `valuation_id` appear more than once in `property_valuation`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `security_id` appear more than once in `loan_security`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q42 &nbsp; ★ &nbsp; (warm-up)

Key uniqueness test: how many values of `postcode` appear more than once in `dim_postcode`? One number (0 = clean).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q43 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan` whose `product_id` has no match in `dim_product.product_id` (ignore NULL `product_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q44 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan` whose `primary_customer_id` has no match in `customer.customer_id` (ignore NULL `primary_customer_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q45 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan` whose `property_id` has no match in `property.property_id` (ignore NULL `property_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q46 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan` whose `assessor_staff_id` has no match in `dim_staff.staff_id` (ignore NULL `assessor_staff_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q47 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_application` whose `primary_customer_id` has no match in `customer.customer_id` (ignore NULL `primary_customer_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q48 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_application` whose `product_id` has no match in `dim_product.product_id` (ignore NULL `product_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q49 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_application` whose `assessor_staff_id` has no match in `dim_staff.staff_id` (ignore NULL `assessor_staff_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q50 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_borrower` whose `customer_id` has no match in `customer.customer_id` (ignore NULL `customer_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q51 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_borrower` whose `loan_id` has no match in `loan.loan_id` (ignore NULL `loan_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q52 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `application_applicant` whose `customer_id` has no match in `customer.customer_id` (ignore NULL `customer_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q53 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `credit_bureau_report` whose `application_id` has no match in `loan_application.application_id` (ignore NULL `application_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q54 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `applicant_income` whose `application_id` has no match in `loan_application.application_id` (ignore NULL `application_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q55 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_security` whose `property_id` has no match in `property.property_id` (ignore NULL `property_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q56 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `property` whose `postcode` has no match in `dim_postcode.postcode` (ignore NULL `postcode`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q57 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `complaint` whose `customer_id` has no match in `customer.customer_id` (ignore NULL `customer_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q58 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `hardship_arrangement` whose `loan_id` has no match in `loan.loan_id` (ignore NULL `loan_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q59 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `loan_event` whose `loan_id` has no match in `loan.loan_id` (ignore NULL `loan_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q60 &nbsp; ★★ &nbsp; (core)

Orphan check: rows in `property_valuation` whose `property_id` has no match in `property.property_id` (ignore NULL `property_id`). Count. One number (0 = clean; if not 0, why?).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q61 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan` where `original_amount` is outside 0 to 5000000 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q62 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan` where `interest_rate_at_origination_pct` is outside 1 to 15 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q63 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan` where `term_months` is outside 12 to 480 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q64 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan` where `lvr_at_origination_pct` is outside 1 to 105 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q65 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan_monthly_snapshot` where `interest_rate_pct` is outside 1 to 15 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q66 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan_monthly_snapshot` where `days_past_due` is outside 0 to 2000 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q67 &nbsp; ★★ &nbsp; (core)

Range check: rows in `credit_bureau_report` where `bureau_score` is outside 300 to 1200 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q68 &nbsp; ★★ &nbsp; (core)

Range check: rows in `loan_application` where `dependants` is outside 0 to 10 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q69 &nbsp; ★★ &nbsp; (core)

Range check: rows in `property` where `bedrooms` is outside 1 to 12 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q70 &nbsp; ★★ &nbsp; (core)

Range check: rows in `property` where `year_built` is outside 1850 to 2026 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q71 &nbsp; ★★ &nbsp; (core)

Range check: rows in `ecl_provision_quarterly` where `lgd` is outside 0 to 1 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q72 &nbsp; ★★ &nbsp; (core)

Range check: rows in `ecl_provision_quarterly` where `pd_12m` is outside 0 to 1 (NULLs excluded). Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q73 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2019: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q74 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2020: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q75 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2021: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q76 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2022: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q77 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2023: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q78 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2024: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q79 &nbsp; ★★★ &nbsp; (challenge)

Snapshot gaps for loans originated in 2025: loans whose snapshot row count is not `MAX(months_on_book)+1`. Count. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
