# 02 - Expressions, CASE and everyday functions

`answers/02_expressions_case_functions/qNN.sql` &nbsp;|&nbsp; check with: `grade 02` or `grade 02 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Computed columns: expressions, CASE and functions

Anything in the SELECT list can be a *calculation*. SQL has no `if` statement - it has **CASE**:

```sql
CASE WHEN lvr_pct > 90 THEN 'High'
     WHEN lvr_pct > 80 THEN 'Elevated'      -- evaluated top to bottom, FIRST match wins
     ELSE 'Standard' END AS lvr_flag
```

```
 lvr_pct   | test 1 (>90) | test 2 (>80) | result
   95.0    |    TRUE      |   (skipped)  | High
   85.0    |    FALSE     |    TRUE      | Elevated
   60.0    |    FALSE     |    FALSE     | Standard   <- falls to ELSE
   NULL    |    unknown   |    unknown   | Standard   <- NULL never satisfies a test!
```

### Function cheat sheet (DuckDB)

| Job | Function |
|---|---|
| round / floor / ceiling | `ROUND(x, 2)`, `FLOOR(x)`, `CEIL(x)` |
| integer division / remainder | `a // b`, `a % b` |
| power | `POWER(x, n)` or `x ** n` |
| biggest / smallest of several columns | `GREATEST(a,b,c)`, `LEAST(a,b,c)` |
| text | `UPPER`, `LOWER`, `TRIM`, `LENGTH`, `LEFT(s,n)`, `RIGHT(s,n)`, `SUBSTR(s,start,len)`, `REPLACE`, `s1 || s2`, `CONCAT_WS(sep, ...)`, `SPLIT_PART(s,'@',2)`, `LPAD(s,4,'0')` |
| change type | `CAST(x AS VARCHAR)` or `x::VARCHAR` |
| fill in NULLs | `COALESCE(a, b, 0)` - first non-NULL |
| turn a value into NULL | `NULLIF(a, 0)` - classic divide-by-zero guard: `x / NULLIF(y, 0)` |

**Integer division trap:** in many databases `7/2` = 3. In DuckDB `7/2` = 3.5 and `7//2` = 3. Know which dialect you are in.

**Loan repayment formula** (monthly principal & interest): with monthly rate `r = rate/1200` and `n` months:
`P * r / (1 - (1+r)^(-n))`

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

For loans 1 to 10 return `loan_id` and the simple principal per month: `original_amount / term_months` rounded to 2 decimals. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Customer full names for `customer_id` 1 to 8 in the form `First Last` (one column, `full_name`), plus `customer_id`. Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Express each product's `max_lvr_pct` as a fraction: return `product_id`, `max_lvr_pct / 100.0` as `max_lvr_fraction`. Sorted by `product_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★ &nbsp; (warm-up)

Term in whole years and leftover months for loans 1-10: `loan_id`, `term_months // 12` (years), `term_months % 12` (months). Sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★ &nbsp; (warm-up)

Round each loan's original amount to the nearest $10,000: `loan_id`, rounded amount, for `loan_id` <= 10. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

`ROUND(x, -4)` rounds to the nearest 10,000.

</details>

### Q06 &nbsp; ★★ &nbsp; (core)

Label each product `Fixed`/`Variable` plus term: return `product_id` and a label like `Fixed 24m` or `Variable` (for variable products). Sorted by `product_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Count loans by LVR band using CASE on `lvr_at_origination_pct`: `'<=60'`, `'60-80'` (above 60 up to and including 80), `'>80'`. Return `lvr_band`, `loans`. Sorted by `loans` descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

CASE is evaluated top to bottom, so the second test only sees rows that failed the first.

</details>

### Q08 &nbsp; ★★ &nbsp; (core)

Debt-to-income bands from `application_assessment`: `'<=4'`, `'4-6'` (above 4 up to and including 6), `'>6'`. Return `dti_band`, `applications`. Sorted by `dti_band`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Simplify application outcomes into three groups using CASE on `current_status`: `'Settled'` -> `'Won'`; `'Declined'` -> `'Declined'`; everything else -> `'Other'`. Return `outcome_group`, `n` (count), sorted by `outcome_group`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Customers whose surname has leading/trailing spaces (a data quality issue): return `customer_id`, `last_name`, sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **132 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Email domains: the part of `email` after the `@`, upper-cased domains are possible so compare in lower case. Return `domain` (lowercased) and `customers`; sorted by `customers` desc, `domain`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

Show NT-style postcodes correctly: from `dim_postcode`, return `postcode` as a 4-character text zero-padded on the left (`'0800'` not `800`) and `suburb`, for the NT only. Sorted by `postcode`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

Mobile numbers: how many customers have a mobile starting with `+61`? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★ &nbsp; (core)

Broker label for applications 1..12: `application_id`, and `COALESCE(CAST(broker_id AS VARCHAR), 'No broker')` as `broker_label`. Sorted by `application_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

For `dim_product` return `product_id` and `annual_fee / NULLIF(max_lvr_pct - 90, 0)` rounded to 2 dp as `weird_ratio` (a deliberately silly metric to practise the divide-by-zero guard). Sorted by `product_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

Does the stored LVR agree with a recalculation? Count loans where `ABS(original_amount / security_value_at_origination * 100 - lvr_at_origination_pct) > 0.01`. One number (should be 0 or tiny).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

Does `assessed_living_expenses` always equal the greater of declared expenses and the HEM benchmark? Join-free check inside `application_assessment` won't have declared expenses, so instead verify: count rows where `hem_applied_flag` is true but `assessed_living_expenses` <> `hem_benchmark_monthly`. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Use GREATEST/LEAST: for `application_assessment` rows with `application_id` <= 10, return `application_id`, `GREATEST(monthly_surplus, 0)` as `positive_surplus` and `LEAST(nsr, 2)` as `capped_nsr`. Sorted by `application_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★★ &nbsp; (challenge)

Compute the contractual monthly P&I repayment for loans 1-15 that are 30-year (`term_months = 360`) variable loans... any loans with `term_months = 360` and `loan_id <= 40`: `P*r/(1-(1+r)^-n)` with `r = interest_rate_at_origination_pct/1200` and `n = term_months`, rounded to 2 dp. Return `loan_id`, `repayment`. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **27 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

`POWER(1 + r, -n)` handles the negative exponent.

</details>

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Stress-test repayment: for the same loans (`term_months = 360`, `loan_id <= 40`) compute the repayment at the original rate **plus 3 percentage points**, and the percentage increase vs the original repayment (rounded to 1 dp). Return `loan_id`, `base_repayment` (2dp), `stressed_repayment` (2dp), `pct_increase` (1dp). Sorted by `loan_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **27 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Classify applications 1-20 into a decision-path label using nested logic: `'Exception approval'` if `policy_exception_flag`; else `'Clean approval'` if `decision = 'Approved'`; else `'Declined - ' || decline_reason_code` if `decision = 'Declined'`; else `'No decision'`. Return `application_id`, `path`, sorted by `application_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **20 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q22 &nbsp; ★★★ &nbsp; (challenge)

The three-valued-logic trap. Count applications where `decision <> 'Approved'` and, separately, where `decision IS DISTINCT FROM 'Approved'`. Return one row with two numbers: `not_equal`, `is_distinct_from`. (They differ because of NULL decisions.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Standardise customer `state` text into the 2-3 letter code using CASE + UPPER/REPLACE: handle `'South Australia'`, `'New South Wales'`, `'Victoria'`, `'Queensland'`, `'Western Australia'`, `'Tasmania'`, `'Northern Territory'` and variants like `'S.A.'`, `'sa'`, `'Vic'`, `'ACT '`. Hint: remove dots and spaces then upper-case, then map long names. Return `state_clean`, `customers` sorted by `state_clean`. You should end up with exactly 8 rows.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

Normalise first in a subquery (`UPPER(REPLACE(REPLACE(state,'.',''),' ',''))`) then map with CASE.

</details>

### Q24 &nbsp; ★ &nbsp; (warm-up)

For the 8 largest loans with purpose `'Purchase - Owner Occupied'` (ties by `loan_id`), show `loan_id`, `original_amount` and the first-year interest at the origination rate: `original_amount * rate / 100` rounded to 2 dp. Largest first.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★ &nbsp; (warm-up)

For the 8 largest loans with purpose `'Purchase - Investment'` (ties by `loan_id`), show `loan_id`, `original_amount` and the first-year interest at the origination rate: `original_amount * rate / 100` rounded to 2 dp. Largest first.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★ &nbsp; (warm-up)

For the 8 largest loans with purpose `'Refinance'` (ties by `loan_id`), show `loan_id`, `original_amount` and the first-year interest at the origination rate: `original_amount * rate / 100` rounded to 2 dp. Largest first.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★ &nbsp; (warm-up)

For the 8 largest loans with purpose `'Equity Release / Top-up'` (ties by `loan_id`), show `loan_id`, `original_amount` and the first-year interest at the origination rate: `original_amount * rate / 100` rounded to 2 dp. Largest first.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★ &nbsp; (warm-up)

For the 8 largest loans with purpose `'Construction'` (ties by `loan_id`), show `loan_id`, `original_amount` and the first-year interest at the origination rate: `original_amount * rate / 100` rounded to 2 dp. Largest first.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★★ &nbsp; (core)

Size-band the `'Broker'` loans originated in 2025 with CASE: `'Small'` under 400,000, `'Mid'` 400,000 to 799,999.99, `'Large'` 800,000 and over. Return `band`, `loans`; sorted by `band`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

Size-band the `'Branch'` loans originated in 2025 with CASE: `'Small'` under 400,000, `'Mid'` 400,000 to 799,999.99, `'Large'` 800,000 and over. Return `band`, `loans`; sorted by `band`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Size-band the `'Digital'` loans originated in 2025 with CASE: `'Small'` under 400,000, `'Mid'` 400,000 to 799,999.99, `'Large'` 800,000 and over. Return `band`, `loans`; sorted by `band`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Size-band the `'Mobile Lender'` loans originated in 2025 with CASE: `'Small'` under 400,000, `'Mid'` 400,000 to 799,999.99, `'Large'` 800,000 and over. Return `band`, `loans`; sorted by `band`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and the surname in upper case (`UPPER`). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and the length of the surname (`LENGTH`). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and the first three letters of the first name (`LEFT`). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and `last_name, first_name` joined as one text value (`||`). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and initials (first letter of first name then first letter of surname). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and the email domain - everything after the `@` (use `SPLIT_PART(email,'@',2)`). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and the email in lower case with spaces trimmed. Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★ &nbsp; (warm-up)

The first 15 customers (by id) that have both an email and a mobile: `customer_id` and the mobile with all spaces removed (`REPLACE`). Sorted by `customer_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★★ &nbsp; (core)

Monthly P&I repayment (2 dp) at the origination rate for loans with a 180-month term and `loan_id <= 200`, first 8 by `loan_id`: `loan_id`, repayment. Formula `P*r/(1-(1+r)^-n)` with `r = rate/1200`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★★ &nbsp; (core)

Monthly P&I repayment (2 dp) at the origination rate for loans with a 240-month term and `loan_id <= 200`, first 8 by `loan_id`: `loan_id`, repayment. Formula `P*r/(1-(1+r)^-n)` with `r = rate/1200`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q43 &nbsp; ★★ &nbsp; (core)

Monthly P&I repayment (2 dp) at the origination rate for loans with a 300-month term and `loan_id <= 200`, first 8 by `loan_id`: `loan_id`, repayment. Formula `P*r/(1-(1+r)^-n)` with `r = rate/1200`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q44 &nbsp; ★★ &nbsp; (core)

Monthly P&I repayment (2 dp) at the origination rate for loans with a 360-month term and `loan_id <= 200`, first 8 by `loan_id`: `loan_id`, repayment. Formula `P*r/(1-(1+r)^-n)` with `r = rate/1200`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q45 &nbsp; ★ &nbsp; (warm-up)

Loans 1-12: `loan_id` and `original_amount` rounded to the nearest $10,000 (`ROUND(x,-4)`). Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q46 &nbsp; ★ &nbsp; (warm-up)

Loans 1-12: `loan_id` and `original_amount` rounded UP to the next $50,000 (`CEIL`). Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q47 &nbsp; ★ &nbsp; (warm-up)

Loans 1-12: `loan_id` and `original_amount` rounded DOWN to the previous $50,000 (`FLOOR`). Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q48 &nbsp; ★ &nbsp; (warm-up)

Loans 1-12: `loan_id` and the LVR as a fraction (`lvr/100`, 4 dp). Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q49 &nbsp; ★ &nbsp; (warm-up)

Loans 1-12: `loan_id` and the loan-to-value shortfall to 80% LVR in dollars: `security_value_at_origination*0.8 - original_amount` (0 dp, may be negative). Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q50 &nbsp; ★★ &nbsp; (core)

Nested CASE: label loans 1-30 `'Prime owner-occ'` if `purpose = 'Purchase - Owner Occupied'` AND LVR <= 80; `'High-LVR owner-occ'` if owner-occupied and LVR > 80; `'Investor'` if `'Purchase - Investment'`; else `'Other'`. Return `loan_id`, `label`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **30 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q51 &nbsp; ★★★ &nbsp; (challenge)

`GREATEST` / `LEAST`: for loans 1-12 return `loan_id` and `GREATEST(original_amount, security_value_at_origination*0.5)` and `LEAST(original_amount, 600000)`. Sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q52 &nbsp; ★★★ &nbsp; (challenge)

Integer division and remainder: for loans 1-12 return `loan_id`, `term_months // 12` (whole years) and `term_months % 12` (leftover months). Sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **12 row(s)** &nbsp;|&nbsp; Sort the output as described.
