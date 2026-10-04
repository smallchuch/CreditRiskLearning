from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="03_nulls", title="03 - NULLs, COALESCE, NULLIF, three-valued logic", primer=PRIMER, problems=[
    P(1, "How many customers have no `date_of_birth` recorded? One number.",
      "SELECT COUNT(*) FROM customer WHERE date_of_birth IS NULL"),
    P(1, "How many loans have a NULL `branch_id`? One number.",
      "SELECT COUNT(*) FROM loan WHERE branch_id IS NULL"),
    P(1, "Return one row with two numbers: the count of ALL rows in `credit_bureau_report` and the count of rows with a non-NULL `bureau_score`.",
      "SELECT COUNT(*), COUNT(bureau_score) FROM credit_bureau_report"),
    P(1, "How many loans are still open, using the fact that `closed_date` is NULL for open loans? (This should equal active + in-recovery loans.) One number.",
      "SELECT COUNT(*) FROM loan WHERE closed_date IS NULL"),
    P(1, "For loans 1 to 15, show `loan_id` and `fixed_rate_expiry_date`, replacing NULL with the date 9999-12-31. Sort by `loan_id`.",
      "SELECT loan_id, COALESCE(fixed_rate_expiry_date, DATE '9999-12-31') FROM loan WHERE loan_id <= 15 ORDER BY loan_id"),
    P(1, "Applications with no decision yet or no final decision recorded: count where `decision IS NULL`, grouped by `current_status`. Return `current_status`, `n`, sorted by `current_status`.",
      "SELECT current_status, COUNT(*) AS n FROM loan_application WHERE decision IS NULL GROUP BY current_status ORDER BY current_status"),
    P(2, "The classic trap. Return one row with two numbers: (a) how many applications have `decision <> 'Approved'`, (b) how many have `decision IS DISTINCT FROM 'Approved'`.",
      "SELECT COUNT(*) FILTER (WHERE decision <> 'Approved'), COUNT(*) FILTER (WHERE decision IS DISTINCT FROM 'Approved') FROM loan_application"),
    P(2, "Broker-channel applications that are missing a broker (`broker_id` NULL): this is a data-quality problem. Return `application_id`, `application_date`, sorted by `application_id`.",
      "SELECT application_id, application_date FROM loan_application WHERE channel='Broker' AND broker_id IS NULL ORDER BY application_id"),
    P(2, "Average bureau score: return two numbers - the plain `AVG(bureau_score)` rounded to 1 dp, and the average if NULL scores were wrongly treated as 0 (`AVG(COALESCE(bureau_score,0))`) rounded to 1 dp. Which would mislead a credit committee?",
      "SELECT ROUND(AVG(bureau_score),1), ROUND(AVG(COALESCE(bureau_score,0)),1) FROM credit_bureau_report"),
    P(2, "For each `income_type` return how many income lines have a NULL `verified_annual_amount` (unverified). Return `income_type`, `unverified_lines`, sorted by `unverified_lines` descending then `income_type`.",
      "SELECT income_type, COUNT(*) AS unverified FROM applicant_income WHERE verified_annual_amount IS NULL GROUP BY 1 ORDER BY 2 DESC, 1"),
    P(2, "Income used for assessment: `COALESCE(verified_annual_amount, declared_annual_amount)`. Return the total of that across all income lines, rounded to 0 dp, as `assessed_income_total`.",
      "SELECT ROUND(SUM(COALESCE(verified_annual_amount, declared_annual_amount)),0) FROM applicant_income"),
    P(2, "Safe division. For loan 1..30 compute `original_amount / NULLIF(io_period_months,0)` rounded to 2 dp (monthly principal-like figure). Return `loan_id`, value; sorted by `loan_id`. Loans with no IO period will show NULL rather than an error.",
      "SELECT loan_id, ROUND(original_amount / NULLIF(io_period_months,0),2) FROM loan WHERE loan_id <= 30 ORDER BY loan_id"),
    P(2, "Count loans by `branch_id`, but show NULL branches as the label `'No branch'`. Return `branch_label` (text), `loans`; sorted by `loans` descending then `branch_label`. Hint: cast the id to text before COALESCE.",
      "SELECT COALESCE(CAST(branch_id AS VARCHAR),'No branch') AS branch_label, COUNT(*) AS loans FROM loan GROUP BY 1 ORDER BY 2 DESC, 1",
      hint="`COALESCE(CAST(branch_id AS VARCHAR), 'No branch')`"),
    P(2, "Loans where `branch_id` is NULL, split by `channel`. Return `channel`, `loans` sorted by `channel`. (What does this tell you about whether NULL is a data error here?)",
      "SELECT channel, COUNT(*) FROM loan WHERE branch_id IS NULL GROUP BY 1 ORDER BY 1"),
    P(2, "Application-level pass rate. For each `channel`, compute the % of applications with `decision = 'Approved'` out of ALL applications (rounded to 1 dp). Return `channel`, `approved_pct`; sorted by `channel`. Careful: `AVG(CASE ... )` vs `COUNT(decision)`.",
      "SELECT channel, ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(*),1) FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Same question but the denominator is only applications that actually reached a decision (`decision IS NOT NULL`). Return `channel`, `approval_rate_pct` (1dp); sorted by `channel`.",
      "SELECT channel, ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1) FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(3, "NULL-safe join key. `loan.application_id` is NULL for internal-refinance child loans. How many loans have a NULL `application_id`, and how many of those have `purpose = 'Internal Refinance'`? Return two numbers.",
      "SELECT COUNT(*), COUNT(*) FILTER (WHERE purpose='Internal Refinance') FROM loan WHERE application_id IS NULL"),
    P(3, "`NOT IN` trap. Count applications that were NOT lodged via a `'Terminated'` broker (`dim_broker.status`). Applications with a NULL `broker_id` must be counted (they have no terminated broker). Return one number. Write it with `NOT EXISTS`; then try `NOT IN` on `broker_id` and see why it breaks.",
      "SELECT COUNT(*) FROM loan_application a WHERE NOT EXISTS (SELECT 1 FROM dim_broker b WHERE b.broker_id = a.broker_id AND b.status='Terminated')"),
    P(3, "Sort with NULLs last. List the 10 loans with the earliest `fixed_rate_expiry_date` that is NOT NULL: return `loan_id`, `fixed_rate_expiry_date`; ties by `loan_id`. Then think about what `ORDER BY ... DESC` would do with NULLs.",
      "SELECT loan_id, fixed_rate_expiry_date FROM loan WHERE fixed_rate_expiry_date IS NOT NULL ORDER BY fixed_rate_expiry_date, loan_id LIMIT 10"),
    P(3, "Customers with a missing DOB: how many of them have also been flagged as duplicates? Duplicates have the same `first_name`, `last_name` (case-insensitive, trimmed) and `postcode`. Return one number: the count of NULL-DOB customers who share lowercase/trimmed name+postcode with at least one other customer.",
      """SELECT COUNT(*) FROM customer c WHERE c.date_of_birth IS NULL AND EXISTS (
  SELECT 1 FROM customer d WHERE d.customer_id <> c.customer_id
    AND LOWER(TRIM(d.first_name)) = LOWER(TRIM(c.first_name)) AND LOWER(TRIM(d.last_name)) = LOWER(TRIM(c.last_name)) AND d.postcode = c.postcode)"""),
    P(3, "Build a single 'bureau quality' label with CASE: `'Thin file'` when `bureau_score IS NULL`, `'Adverse'` when `bankruptcy_flag` or `court_judgements > 0`, `'Weak'` when score < 600, `'Fair'` when 600-749, else `'Strong'`. Return `quality`, `reports` ordered by `reports` descending, then `quality`. Order of the CASE branches matters.",
      """SELECT CASE WHEN bureau_score IS NULL THEN 'Thin file' WHEN bankruptcy_flag OR court_judgements > 0 THEN 'Adverse'
  WHEN bureau_score < 600 THEN 'Weak' WHEN bureau_score < 750 THEN 'Fair' ELSE 'Strong' END AS quality, COUNT(*) AS reports
FROM credit_bureau_report GROUP BY 1 ORDER BY 2 DESC, 1"""),
])
