# 01 - SELECT, WHERE, ORDER BY, LIMIT, DISTINCT

`answers/01_select_filter_sort/qNN.sql` &nbsp;|&nbsp; check with: `grade 01` or `grade 01 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## The one sentence every query is built from

```
SELECT    what columns / calculations do I want to see?
FROM      which table?
WHERE     which ROWS survive?                      (filters rows BEFORE grouping)
ORDER BY  in what order?
LIMIT     how many rows?
```

SQL is *written* in that order but *runs* in a different order - this explains most "why can't I use my alias there?" errors:

```
 1. FROM        pick the table
 2. WHERE       throw away rows that fail the test
 3. SELECT      compute the columns (aliases are born here)
 4. DISTINCT    remove duplicate result rows
 5. ORDER BY    sort (can use aliases - they exist now)
 6. LIMIT       keep the first N rows
```

### Row-by-row walkthrough

`SELECT loan_id, original_amount FROM loan WHERE original_amount > 900000 ORDER BY original_amount DESC LIMIT 3`

```
 loan table (5 of 67,271 rows)          WHERE amount > 900000        ORDER BY amount DESC      LIMIT 3
 loan_id | original_amount              loan_id | amount             loan_id | amount          loan_id | amount
    1    |   286,000     x dropped         5    | 1,150,000             9    | 2,300,000          9    | 2,300,000
    5    | 1,150,000     v kept            9    | 2,300,000             5    | 1,150,000          5    | 1,150,000
    9    | 2,300,000     v kept            7    |   980,000             7    |   980,000          7    |   980,000
    7    |   980,000     v kept
    3    |   546,000     x dropped
```

### Filter toolbox

| You want | Write |
|---|---|
| equals / not equals | `= `, `<>` (or `!=`) |
| range (inclusive both ends) | `BETWEEN 500000 AND 750000` |
| one of a list | `IN ('SA','VIC','WA')` |
| text pattern | `LIKE 'Mt%'` (`%` = any chars, `_` = one char), `ILIKE` ignores case |
| combine | `AND`, `OR`, `NOT` - use brackets: `A AND (B OR C)` |
| missing value | `IS NULL` / `IS NOT NULL` (never `= NULL`) |
| unique values | `SELECT DISTINCT col` |

**Gotcha:** `AND` binds tighter than `OR`. `a OR b AND c` means `a OR (b AND c)`.

**Dates** are written `DATE '2024-06-30'` (or just `'2024-06-30'`).

Tables used here: `loan`, `loan_application`, `customer`, `dim_product`, `dim_branch`, `dim_broker`, `property`, `dim_staff`.
Open `DATA_DICTIONARY.md` (in Datasets/Synthetic Bank) whenever you need a column.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

List every product: `product_id`, `product_name`, `rate_type`. Sort by `product_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

How many rows are in the `loan` table? Return one number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Show `loan_id`, `original_amount`, `origination_date` for loans with an original amount over $1,500,000. Sort by amount (largest first), then `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1,778 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q04 &nbsp; ★ &nbsp; (warm-up)

List the distinct `purpose` values on the `loan` table, sorted alphabetically.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★ &nbsp; (warm-up)

Show the 10 most recently settled loans: `loan_id`, `origination_date`, `original_amount`. Latest date first; break ties by `loan_id` descending.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★ &nbsp; (warm-up)

Which branches are in South Australia? Return `branch_id`, `branch_name`, sorted by `branch_name`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **18 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★ &nbsp; (warm-up)

Loans with a fixed interest rate: return `loan_id`, `interest_rate_at_origination_pct`, `fixed_rate_expiry_date` for loans originated in 2021 with `rate_type = 'Fixed'`, sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3,987 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

A date range is safest as `>= start AND < next start` - it works even when the column has a time part.

</details>

### Q08 &nbsp; ★ &nbsp; (warm-up)

Loans with an original amount between $400,000 and $450,000 inclusive, that are still `Active`. Return `loan_id`, `original_amount`, sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3,674 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★ &nbsp; (core)

Applications for either `'Construction'` or `'Equity Release / Top-up'` purposes that were `Declined`. Return `application_id`, `purpose`, `decline_reason_code`; sorted by `application_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4,222 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★ &nbsp; (core)

Customers whose surname starts with `Mc`. Return `customer_id`, `first_name`, `last_name` sorted by `last_name`, `first_name`, `customer_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **665 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★ &nbsp; (core)

Suburbs (`dim_postcode`) in `'NSW'` or `'VIC'` that are `'Regional'` market segment. Return `postcode`, `suburb`, `state`, sorted by `state`, `suburb`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★ &nbsp; (core)

Loans that are NOT owner-occupied-purchase and NOT refinance: return `loan_id`, `purpose` for purposes other than `'Purchase - Owner Occupied'` and `'Refinance'` that originated in December 2025. Sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **650 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

Brokers who are not `'Active'`: `broker_id`, `firm_name`, `status`, `status_change_date`. Sort by `status_change_date` (oldest first), then `broker_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **61 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q14 &nbsp; ★★ &nbsp; (core)

Loans with LVR above 90% that did NOT require mortgage insurance (`lmi_flag` false) - a possible data problem. Return `loan_id`, `lvr_at_origination_pct`, sorted by `loan_id`. (It may return 0 rows - that is fine and the checker accepts that.)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **0 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q15 &nbsp; ★★ &nbsp; (core)

Applications that were approved with a policy exception AND for an amount of at least $800,000. Return `application_id`, `requested_amount`, `policy_exception_reason`, sorted by `requested_amount` descending then `application_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **76 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q16 &nbsp; ★★ &nbsp; (core)

Loans with an interest-only period: return `loan_id`, `io_period_months`, `io_expiry_date` for loans that have `io_period_months > 0` and an `io_expiry_date` on or before 2025-12-31 and are still `Active`. Sort by `io_expiry_date`, `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2,269 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q17 &nbsp; ★★ &nbsp; (core)

How many distinct customers ever applied as the primary applicant? One number (`primary_customer_id` on `loan_application`).

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

Distinct combinations that exist in `dim_product`: return the three columns (`rate_type`, `repayment_type`, `occupancy`) sorted by all three.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q19 &nbsp; ★★ &nbsp; (core)

The 5 largest loans originated through the `'Broker'` channel that are still `Active`: `loan_id`, `original_amount`. Largest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q20 &nbsp; ★★★ &nbsp; (challenge)

Applications that are 'in flight' at the snapshot date: `current_status` is `'In Progress'` or `'Approved - Awaiting Settlement'`, AND the application was lodged on or after 2025-12-01. Return `application_id`, `application_date`, `current_status`, sorted by `application_date`, `application_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1,933 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q21 &nbsp; ★★★ &nbsp; (challenge)

Precedence trap. Loans where (`purpose` = 'Purchase - Investment' OR `purpose` = 'Construction') AND `original_amount` > 1200000 AND `origination_date` >= 2024-01-01. Return `loan_id`, `purpose`, `original_amount`; sorted by `loan_id`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **567 row(s)** &nbsp;|&nbsp; Sort the output as described.

<details><summary>hint</summary>

Without brackets `A OR B AND C` would give the wrong rows.

</details>

### Q22 &nbsp; ★★★ &nbsp; (challenge)

Staff who have left the bank: `staff_id`, `full_name`, `team`, `termination_date` where `termination_date` is not null and falls in calendar year 2024. Sorted by `termination_date`, `staff_id`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Properties: houses with at least 4 bedrooms and a land area over 1,000 sqm built after 2010. Return `property_id`, `bedrooms`, `land_area_sqm`, `year_built`; sorted by `land_area_sqm` desc, `property_id`. Use only the `property` table.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **781 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q24 &nbsp; ★★★ &nbsp; (challenge)

Find loans originated on a weekend. (Settlements should happen on business days.) Use `strftime('%w', date)` or `dayofweek(date)` - in DuckDB `dayofweek` gives 0=Sunday..6=Saturday. Return `loan_id`, `origination_date`, sorted by `loan_id`. Probably 0 rows.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **925 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q25 &nbsp; ★ &nbsp; (warm-up)

Loans with purpose `'Purchase - Owner Occupied'` originated in 2023 with an original amount over $500,000: return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q26 &nbsp; ★ &nbsp; (warm-up)

Loans with purpose `'Purchase - Investment'` originated in 2023 with an original amount over $500,000: return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q27 &nbsp; ★ &nbsp; (warm-up)

Loans with purpose `'Refinance'` originated in 2023 with an original amount over $500,000: return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q28 &nbsp; ★ &nbsp; (warm-up)

Loans with purpose `'Equity Release / Top-up'` originated in 2023 with an original amount over $500,000: return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q29 &nbsp; ★ &nbsp; (warm-up)

Loans with purpose `'Construction'` originated in 2023 with an original amount over $500,000: return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q30 &nbsp; ★★ &nbsp; (core)

Active loans written through the `'Broker'` channel with an origination LVR above 85: `loan_id`, `lvr_at_origination_pct`; highest LVR first, ties by `loan_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★ &nbsp; (core)

Active loans written through the `'Branch'` channel with an origination LVR above 85: `loan_id`, `lvr_at_origination_pct`; highest LVR first, ties by `loan_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★ &nbsp; (core)

Active loans written through the `'Digital'` channel with an origination LVR above 85: `loan_id`, `lvr_at_origination_pct`; highest LVR first, ties by `loan_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★ &nbsp; (core)

Active loans written through the `'Mobile Lender'` channel with an origination LVR above 85: `loan_id`, `lvr_at_origination_pct`; highest LVR first, ties by `loan_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★ &nbsp; (warm-up)

Branches in `'NSW'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★ &nbsp; (warm-up)

Branches in `'VIC'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q36 &nbsp; ★ &nbsp; (warm-up)

Branches in `'QLD'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **7 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q37 &nbsp; ★ &nbsp; (warm-up)

Branches in `'SA'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **18 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q38 &nbsp; ★ &nbsp; (warm-up)

Branches in `'WA'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q39 &nbsp; ★ &nbsp; (warm-up)

Postcodes in `'NSW'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by `postcode`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q40 &nbsp; ★ &nbsp; (warm-up)

Postcodes in `'VIC'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by `postcode`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **15 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q41 &nbsp; ★ &nbsp; (warm-up)

Postcodes in `'QLD'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by `postcode`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **11 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q42 &nbsp; ★ &nbsp; (warm-up)

Postcodes in `'SA'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by `postcode`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **35 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q43 &nbsp; ★ &nbsp; (warm-up)

Postcodes in `'WA'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by `postcode`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q44 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2019: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q45 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2020: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q46 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2021: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q47 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2022: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q48 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2023: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q49 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2024: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q50 &nbsp; ★★ &nbsp; (core)

The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2025: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **5 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q51 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with `current_status = 'Settled'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q52 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with `current_status = 'Declined'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q53 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with `current_status = 'Withdrawn'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q54 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with `current_status = 'Lapsed'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q55 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with `current_status = 'In Progress'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q56 &nbsp; ★★ &nbsp; (core)

Applications lodged in 2025 with `current_status = 'Approved - Awaiting Settlement'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q57 &nbsp; ★★★ &nbsp; (challenge)

Loans originated on a month-end day (the 28th-31st) in 2025 AND over $700,000 OR with LVR above 95. Careful with brackets: `(amount > 700000 OR lvr > 95)` is the second condition. Return `loan_id`, `origination_date`; sorted by `loan_id`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **495 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q58 &nbsp; ★★★ &nbsp; (challenge)

Distinct combinations of `channel` and `purpose` for loans originated in 2025: sorted by `channel`, `purpose`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **21 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q59 &nbsp; ★★★ &nbsp; (challenge)

Skip the first 20 and take the next 10: loans ordered by `original_amount` descending, `loan_id` ascending - return `loan_id`, `original_amount` for ranks 21-30 (use `OFFSET`).

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.
