from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="02_expressions_case_functions", title="02 - Expressions, CASE and everyday functions", primer=PRIMER, problems=[
    P(1, "For loans 1 to 10 return `loan_id` and the simple principal per month: `original_amount / term_months` rounded to 2 decimals. Sorted by `loan_id`.",
      "SELECT loan_id, ROUND(original_amount / term_months, 2) FROM loan WHERE loan_id <= 10 ORDER BY loan_id"),
    P(1, "Customer full names for `customer_id` 1 to 8 in the form `First Last` (one column, `full_name`), plus `customer_id`. Sorted by `customer_id`.",
      "SELECT customer_id, first_name || ' ' || last_name AS full_name FROM customer WHERE customer_id <= 8 ORDER BY customer_id"),
    P(1, "Express each product's `max_lvr_pct` as a fraction: return `product_id`, `max_lvr_pct / 100.0` as `max_lvr_fraction`. Sorted by `product_id`.",
      "SELECT product_id, max_lvr_pct / 100.0 FROM dim_product ORDER BY product_id"),
    P(1, "Term in whole years and leftover months for loans 1-10: `loan_id`, `term_months // 12` (years), `term_months % 12` (months). Sorted by `loan_id`.",
      "SELECT loan_id, term_months // 12, term_months % 12 FROM loan WHERE loan_id <= 10 ORDER BY loan_id"),
    P(1, "Round each loan's original amount to the nearest $10,000: `loan_id`, rounded amount, for `loan_id` <= 10. Sorted by `loan_id`.",
      "SELECT loan_id, ROUND(original_amount, -4) FROM loan WHERE loan_id <= 10 ORDER BY loan_id",
      hint="`ROUND(x, -4)` rounds to the nearest 10,000."),
    P(2, "Label each product `Fixed`/`Variable` plus term: return `product_id` and a label like `Fixed 24m` or `Variable` (for variable products). Sorted by `product_id`.",
      "SELECT product_id, CASE WHEN rate_type='Fixed' THEN 'Fixed ' || fixed_term_months || 'm' ELSE 'Variable' END FROM dim_product ORDER BY product_id"),
    P(2, "Count loans by LVR band using CASE on `lvr_at_origination_pct`: `'<=60'`, `'60-80'` (above 60 up to and including 80), `'>80'`. Return `lvr_band`, `loans`. Sorted by `loans` descending.",
      "SELECT CASE WHEN lvr_at_origination_pct <= 60 THEN '<=60' WHEN lvr_at_origination_pct <= 80 THEN '60-80' ELSE '>80' END AS lvr_band, COUNT(*) AS loans FROM loan GROUP BY 1 ORDER BY 2 DESC",
      hint="CASE is evaluated top to bottom, so the second test only sees rows that failed the first."),
    P(2, "Debt-to-income bands from `application_assessment`: `'<=4'`, `'4-6'` (above 4 up to and including 6), `'>6'`. Return `dti_band`, `applications`. Sorted by `dti_band`.",
      "SELECT CASE WHEN dti_ratio <= 4 THEN '<=4' WHEN dti_ratio <= 6 THEN '4-6' ELSE '>6' END AS dti_band, COUNT(*) FROM application_assessment GROUP BY 1 ORDER BY 1"),
    P(2, "Simplify application outcomes into three groups using CASE on `current_status`: `'Settled'` -> `'Won'`; `'Declined'` -> `'Declined'`; everything else -> `'Other'`. Return `outcome_group`, `n` (count), sorted by `outcome_group`.",
      "SELECT CASE current_status WHEN 'Settled' THEN 'Won' WHEN 'Declined' THEN 'Declined' ELSE 'Other' END AS outcome_group, COUNT(*) n FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Customers whose surname has leading/trailing spaces (a data quality issue): return `customer_id`, `last_name`, sorted by `customer_id`.",
      "SELECT customer_id, last_name FROM customer WHERE last_name <> TRIM(last_name) ORDER BY customer_id"),
    P(2, "Email domains: the part of `email` after the `@`, upper-cased domains are possible so compare in lower case. Return `domain` (lowercased) and `customers`; sorted by `customers` desc, `domain`.",
      "SELECT LOWER(SPLIT_PART(email, '@', 2)) AS domain, COUNT(*) AS customers FROM customer GROUP BY 1 ORDER BY 2 DESC, 1"),
    P(2, "Show NT-style postcodes correctly: from `dim_postcode`, return `postcode` as a 4-character text zero-padded on the left (`'0800'` not `800`) and `suburb`, for the NT only. Sorted by `postcode`.",
      "SELECT LPAD(CAST(postcode AS VARCHAR), 4, '0') AS postcode_txt, suburb FROM dim_postcode WHERE state='NT' ORDER BY postcode"),
    P(2, "Mobile numbers: how many customers have a mobile starting with `+61`? One number.",
      "SELECT COUNT(*) FROM customer WHERE mobile LIKE '+61%'"),
    P(2, "Broker label for applications 1..12: `application_id`, and `COALESCE(CAST(broker_id AS VARCHAR), 'No broker')` as `broker_label`. Sorted by `application_id`.",
      "SELECT application_id, COALESCE(CAST(broker_id AS VARCHAR), 'No broker') FROM loan_application WHERE application_id <= 12 ORDER BY application_id"),
    P(2, "For `dim_product` return `product_id` and `annual_fee / NULLIF(max_lvr_pct - 90, 0)` rounded to 2 dp as `weird_ratio` (a deliberately silly metric to practise the divide-by-zero guard). Sorted by `product_id`.",
      "SELECT product_id, ROUND(annual_fee / NULLIF(max_lvr_pct - 90, 0), 2) FROM dim_product ORDER BY product_id"),
    P(2, "Does the stored LVR agree with a recalculation? Count loans where `ABS(original_amount / security_value_at_origination * 100 - lvr_at_origination_pct) > 0.01`. One number (should be 0 or tiny).",
      "SELECT COUNT(*) FROM loan WHERE ABS(original_amount / security_value_at_origination * 100 - lvr_at_origination_pct) > 0.01", empty_ok=True),
    P(2, "Does `assessed_living_expenses` always equal the greater of declared expenses and the HEM benchmark? Join-free check inside `application_assessment` won't have declared expenses, so instead verify: count rows where `hem_applied_flag` is true but `assessed_living_expenses` <> `hem_benchmark_monthly`. One number.",
      "SELECT COUNT(*) FROM application_assessment WHERE hem_applied_flag AND assessed_living_expenses <> hem_benchmark_monthly"),
    P(2, "Use GREATEST/LEAST: for `application_assessment` rows with `application_id` <= 10, return `application_id`, `GREATEST(monthly_surplus, 0)` as `positive_surplus` and `LEAST(nsr, 2)` as `capped_nsr`. Sorted by `application_id`.",
      "SELECT application_id, GREATEST(monthly_surplus, 0), LEAST(nsr, 2) FROM application_assessment WHERE application_id <= 10 ORDER BY application_id"),
    P(3, "Compute the contractual monthly P&I repayment for loans 1-15 that are 30-year (`term_months = 360`) variable loans... any loans with `term_months = 360` and `loan_id <= 40`: `P*r/(1-(1+r)^-n)` with `r = interest_rate_at_origination_pct/1200` and `n = term_months`, rounded to 2 dp. Return `loan_id`, `repayment`. Sorted by `loan_id`.",
      "SELECT loan_id, ROUND(original_amount * (interest_rate_at_origination_pct/1200) / (1 - POWER(1 + interest_rate_at_origination_pct/1200, -term_months)), 2) FROM loan WHERE term_months = 360 AND loan_id <= 40 ORDER BY loan_id",
      hint="`POWER(1 + r, -n)` handles the negative exponent."),
    P(3, "Stress-test repayment: for the same loans (`term_months = 360`, `loan_id <= 40`) compute the repayment at the original rate **plus 3 percentage points**, and the percentage increase vs the original repayment (rounded to 1 dp). Return `loan_id`, `base_repayment` (2dp), `stressed_repayment` (2dp), `pct_increase` (1dp). Sorted by `loan_id`.",
      """WITH r AS (
  SELECT loan_id, original_amount AS p, term_months AS n, interest_rate_at_origination_pct/1200 AS r0, (interest_rate_at_origination_pct+3)/1200 AS r1
  FROM loan WHERE term_months = 360 AND loan_id <= 40)
SELECT loan_id, ROUND(p*r0/(1-POWER(1+r0,-n)),2) AS base,
       ROUND(p*r1/(1-POWER(1+r1,-n)),2) AS stressed,
       ROUND(100*((p*r1/(1-POWER(1+r1,-n)))/(p*r0/(1-POWER(1+r0,-n)))-1),1) AS pct_increase
FROM r ORDER BY loan_id"""),
    P(3, "Classify applications 1-20 into a decision-path label using nested logic: `'Exception approval'` if `policy_exception_flag`; else `'Clean approval'` if `decision = 'Approved'`; else `'Declined - ' || decline_reason_code` if `decision = 'Declined'`; else `'No decision'`. Return `application_id`, `path`, sorted by `application_id`.",
      "SELECT application_id, CASE WHEN policy_exception_flag THEN 'Exception approval' WHEN decision='Approved' THEN 'Clean approval' WHEN decision='Declined' THEN 'Declined - ' || decline_reason_code ELSE 'No decision' END FROM loan_application WHERE application_id <= 20 ORDER BY application_id"),
    P(3, "The three-valued-logic trap. Count applications where `decision <> 'Approved'` and, separately, where `decision IS DISTINCT FROM 'Approved'`. Return one row with two numbers: `not_equal`, `is_distinct_from`. (They differ because of NULL decisions.)",
      "SELECT COUNT(*) FILTER (WHERE decision <> 'Approved'), COUNT(*) FILTER (WHERE decision IS DISTINCT FROM 'Approved') FROM loan_application"),
    P(3, "Standardise customer `state` text into the 2-3 letter code using CASE + UPPER/REPLACE: handle `'South Australia'`, `'New South Wales'`, `'Victoria'`, `'Queensland'`, `'Western Australia'`, `'Tasmania'`, `'Northern Territory'` and variants like `'S.A.'`, `'sa'`, `'Vic'`, `'ACT '`. Hint: remove dots and spaces then upper-case, then map long names. Return `state_clean`, `customers` sorted by `state_clean`. You should end up with exactly 8 rows.",
      """SELECT CASE s WHEN 'SOUTHAUSTRALIA' THEN 'SA' WHEN 'NEWSOUTHWALES' THEN 'NSW' WHEN 'VICTORIA' THEN 'VIC' WHEN 'QUEENSLAND' THEN 'QLD'
       WHEN 'WESTERNAUSTRALIA' THEN 'WA' WHEN 'TASMANIA' THEN 'TAS' WHEN 'NORTHERNTERRITORY' THEN 'NT' ELSE s END AS state_clean, COUNT(*) AS customers
FROM (SELECT UPPER(REPLACE(REPLACE(state,'.',''),' ','')) AS s FROM customer) GROUP BY 1 ORDER BY 1""",
      hint="Normalise first in a subquery (`UPPER(REPLACE(REPLACE(state,'.',''),' ',''))`) then map with CASE."),
])
