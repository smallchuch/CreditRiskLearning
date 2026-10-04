from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="01_select_filter_sort", title="01 - SELECT, WHERE, ORDER BY, LIMIT, DISTINCT", primer=PRIMER, problems=[
    P(1, "List every product: `product_id`, `product_name`, `rate_type`. Sort by `product_id`.",
      "SELECT product_id, product_name, rate_type FROM dim_product ORDER BY product_id"),
    P(1, "How many rows are in the `loan` table? Return one number.",
      "SELECT COUNT(*) FROM loan"),
    P(1, "Show `loan_id`, `original_amount`, `origination_date` for loans with an original amount over $1,500,000. Sort by amount (largest first), then `loan_id`.",
      "SELECT loan_id, original_amount, origination_date FROM loan WHERE original_amount > 1500000 ORDER BY original_amount DESC, loan_id"),
    P(1, "List the distinct `purpose` values on the `loan` table, sorted alphabetically.",
      "SELECT DISTINCT purpose FROM loan ORDER BY purpose"),
    P(1, "Show the 10 most recently settled loans: `loan_id`, `origination_date`, `original_amount`. Latest date first; break ties by `loan_id` descending.",
      "SELECT loan_id, origination_date, original_amount FROM loan ORDER BY origination_date DESC, loan_id DESC LIMIT 10"),
    P(1, "Which branches are in South Australia? Return `branch_id`, `branch_name`, sorted by `branch_name`.",
      "SELECT branch_id, branch_name FROM dim_branch WHERE state = 'SA' ORDER BY branch_name"),
    P(1, "Loans with a fixed interest rate: return `loan_id`, `interest_rate_at_origination_pct`, `fixed_rate_expiry_date` for loans originated in 2021 with `rate_type = 'Fixed'`, sorted by `loan_id`.",
      "SELECT loan_id, interest_rate_at_origination_pct, fixed_rate_expiry_date FROM loan WHERE rate_type='Fixed' AND origination_date >= DATE '2021-01-01' AND origination_date < DATE '2022-01-01' ORDER BY loan_id",
      hint="A date range is safest as `>= start AND < next start` - it works even when the column has a time part."),
    P(1, "Loans with an original amount between $400,000 and $450,000 inclusive, that are still `Active`. Return `loan_id`, `original_amount`, sorted by `loan_id`.",
      "SELECT loan_id, original_amount FROM loan WHERE original_amount BETWEEN 400000 AND 450000 AND loan_status='Active' ORDER BY loan_id"),
    P(2, "Applications for either `'Construction'` or `'Equity Release / Top-up'` purposes that were `Declined`. Return `application_id`, `purpose`, `decline_reason_code`; sorted by `application_id`.",
      "SELECT application_id, purpose, decline_reason_code FROM loan_application WHERE purpose IN ('Construction','Equity Release / Top-up') AND current_status='Declined' ORDER BY application_id"),
    P(2, "Customers whose surname starts with `Mc`. Return `customer_id`, `first_name`, `last_name` sorted by `last_name`, `first_name`, `customer_id`.",
      "SELECT customer_id, first_name, last_name FROM customer WHERE last_name LIKE 'Mc%' ORDER BY last_name, first_name, customer_id"),
    P(2, "Suburbs (`dim_postcode`) in `'NSW'` or `'VIC'` that are `'Regional'` market segment. Return `postcode`, `suburb`, `state`, sorted by `state`, `suburb`.",
      "SELECT postcode, suburb, state FROM dim_postcode WHERE state IN ('NSW','VIC') AND market_segment='Regional' ORDER BY state, suburb"),
    P(2, "Loans that are NOT owner-occupied-purchase and NOT refinance: return `loan_id`, `purpose` for purposes other than `'Purchase - Owner Occupied'` and `'Refinance'` that originated in December 2025. Sorted by `loan_id`.",
      "SELECT loan_id, purpose FROM loan WHERE purpose NOT IN ('Purchase - Owner Occupied','Refinance') AND origination_date >= DATE '2025-12-01' AND origination_date <= DATE '2025-12-31' ORDER BY loan_id"),
    P(2, "Brokers who are not `'Active'`: `broker_id`, `firm_name`, `status`, `status_change_date`. Sort by `status_change_date` (oldest first), then `broker_id`.",
      "SELECT broker_id, firm_name, status, status_change_date FROM dim_broker WHERE status <> 'Active' ORDER BY status_change_date, broker_id"),
    P(2, "Loans with LVR above 90% that did NOT require mortgage insurance (`lmi_flag` false) - a possible data problem. Return `loan_id`, `lvr_at_origination_pct`, sorted by `loan_id`. (It may return 0 rows - that is fine and the checker accepts that.)",
      "SELECT loan_id, lvr_at_origination_pct FROM loan WHERE lvr_at_origination_pct > 90 AND NOT lmi_flag ORDER BY loan_id", empty_ok=True),
    P(2, "Applications that were approved with a policy exception AND for an amount of at least $800,000. Return `application_id`, `requested_amount`, `policy_exception_reason`, sorted by `requested_amount` descending then `application_id`.",
      "SELECT application_id, requested_amount, policy_exception_reason FROM loan_application WHERE policy_exception_flag AND requested_amount >= 800000 ORDER BY requested_amount DESC, application_id"),
    P(2, "Loans with an interest-only period: return `loan_id`, `io_period_months`, `io_expiry_date` for loans that have `io_period_months > 0` and an `io_expiry_date` on or before 2025-12-31 and are still `Active`. Sort by `io_expiry_date`, `loan_id`.",
      "SELECT loan_id, io_period_months, io_expiry_date FROM loan WHERE io_period_months > 0 AND io_expiry_date <= DATE '2025-12-31' AND loan_status='Active' ORDER BY io_expiry_date, loan_id"),
    P(2, "How many distinct customers ever applied as the primary applicant? One number (`primary_customer_id` on `loan_application`).",
      "SELECT COUNT(DISTINCT primary_customer_id) FROM loan_application"),
    P(2, "Distinct combinations that exist in `dim_product`: return the three columns (`rate_type`, `repayment_type`, `occupancy`) sorted by all three.",
      "SELECT DISTINCT rate_type, repayment_type, occupancy FROM dim_product ORDER BY 1,2,3"),
    P(2, "The 5 largest loans originated through the `'Broker'` channel that are still `Active`: `loan_id`, `original_amount`. Largest first, ties by `loan_id`.",
      "SELECT loan_id, original_amount FROM loan WHERE channel='Broker' AND loan_status='Active' ORDER BY original_amount DESC, loan_id LIMIT 5"),
    P(3, "Applications that are 'in flight' at the snapshot date: `current_status` is `'In Progress'` or `'Approved - Awaiting Settlement'`, AND the application was lodged on or after 2025-12-01. Return `application_id`, `application_date`, `current_status`, sorted by `application_date`, `application_id`.",
      "SELECT application_id, application_date, current_status FROM loan_application WHERE current_status IN ('In Progress','Approved - Awaiting Settlement') AND application_date >= DATE '2025-12-01' ORDER BY application_date, application_id"),
    P(3, "Precedence trap. Loans where (`purpose` = 'Purchase - Investment' OR `purpose` = 'Construction') AND `original_amount` > 1200000 AND `origination_date` >= 2024-01-01. Return `loan_id`, `purpose`, `original_amount`; sorted by `loan_id`.",
      "SELECT loan_id, purpose, original_amount FROM loan WHERE (purpose = 'Purchase - Investment' OR purpose = 'Construction') AND original_amount > 1200000 AND origination_date >= DATE '2024-01-01' ORDER BY loan_id",
      hint="Without brackets `A OR B AND C` would give the wrong rows."),
    P(3, "Staff who have left the bank: `staff_id`, `full_name`, `team`, `termination_date` where `termination_date` is not null and falls in calendar year 2024. Sorted by `termination_date`, `staff_id`.",
      "SELECT staff_id, full_name, team, termination_date FROM dim_staff WHERE termination_date >= DATE '2024-01-01' AND termination_date < DATE '2025-01-01' ORDER BY termination_date, staff_id"),
    P(3, "Properties: houses with at least 4 bedrooms and a land area over 1,000 sqm built after 2010. Return `property_id`, `bedrooms`, `land_area_sqm`, `year_built`; sorted by `land_area_sqm` desc, `property_id`. Use only the `property` table.",
      "SELECT property_id, bedrooms, land_area_sqm, year_built FROM property WHERE property_type='House' AND bedrooms >= 4 AND land_area_sqm > 1000 AND year_built > 2010 ORDER BY land_area_sqm DESC, property_id"),
    P(3, "Find loans originated on a weekend. (Settlements should happen on business days.) Use `strftime('%w', date)` or `dayofweek(date)` - in DuckDB `dayofweek` gives 0=Sunday..6=Saturday. Return `loan_id`, `origination_date`, sorted by `loan_id`. Probably 0 rows.",
      "SELECT loan_id, origination_date FROM loan WHERE dayofweek(origination_date) IN (0,6) ORDER BY loan_id", empty_ok=True),
])
