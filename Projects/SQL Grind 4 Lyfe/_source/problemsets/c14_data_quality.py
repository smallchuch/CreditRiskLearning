from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="14_data_quality", title="14 - Data quality: duplicates, orphans, ranges, gaps and islands", primer=PRIMER, problems=[
    P(1, "Duplicate keys test: is `loan_id` unique on `loan`? Return the number of `loan_id` values that appear more than once (0 expected). One number.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan GROUP BY 1 HAVING COUNT(*)>1)"),
    P(1, "Orphan check: loans whose `product_id` is not in `dim_product`. Count. One number.",
      "SELECT COUNT(*) FROM loan l WHERE NOT EXISTS (SELECT 1 FROM dim_product p WHERE p.product_id=l.product_id)"),
    P(1, "Range check: loans with `lvr_at_origination_pct` outside 0-100 (a loan can't be below 0; above 100 might happen with capitalised costs - count both ways). Return two numbers: below 0, above 100.",
      "SELECT COUNT(*) FILTER (WHERE lvr_at_origination_pct<0), COUNT(*) FILTER (WHERE lvr_at_origination_pct>100) FROM loan"),
    P(1, "Valuation zeros: how many rows in `property_valuation` have `valuation_amount = 0`, grouped by `valuation_type`? Return `valuation_type`, `zero_rows`; sorted by type, only types with at least one zero.",
      "SELECT valuation_type, COUNT(*) FROM property_valuation WHERE valuation_amount=0 GROUP BY 1 HAVING COUNT(*)>0 ORDER BY 1"),
    P(2, "Duplicate customers by normalised name + DOB: groups of rows with the same `LOWER(TRIM(first_name))`, `LOWER(TRIM(last_name))` and `date_of_birth` (non-null). Return the number of duplicate GROUPS. One number.",
      "SELECT COUNT(*) FROM (SELECT 1 FROM customer WHERE date_of_birth IS NOT NULL GROUP BY LOWER(TRIM(first_name)), LOWER(TRIM(last_name)), date_of_birth HAVING COUNT(*)>1)"),
    P(2, "Messy state values: list every distinct raw `state` value that is NOT one of the 8 clean codes ('NSW','VIC','QLD','SA','WA','TAS','NT','ACT'). Return `state`, `n`; sorted by `n` descending then `state`.",
      "SELECT state, COUNT(*) AS n FROM customer WHERE state NOT IN ('NSW','VIC','QLD','SA','WA','TAS','NT','ACT') GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "Mobile formats: classify `mobile` as `'04xxxxxxxx'` (starts with `04` and is 10 chars), `'+61 prefix'` (starts with `+61`), or `'other'`; NULL mobile as `'missing'`. Return `format`, `customers`; sorted by `format`.",
      "SELECT CASE WHEN mobile IS NULL THEN 'missing' WHEN mobile LIKE '04%' AND LENGTH(mobile)=10 THEN '04xxxxxxxx' WHEN mobile LIKE '+61%' THEN '+61 prefix' ELSE 'other' END AS f, COUNT(*) FROM customer GROUP BY 1 ORDER BY 1"),
    P(2, "Email case: how many customers have an email that is not entirely lowercase (`email <> LOWER(email)`)? One number.",
      "SELECT COUNT(*) FROM customer WHERE email <> LOWER(email)"),
    P(2, "Date logic: loans with `closed_date < origination_date`. Count. (Expect 0.) One number.",
      "SELECT COUNT(*) FROM loan WHERE closed_date < origination_date"),
    P(2, "Status vs date consistency: loans with `loan_status = 'Closed'` but NULL `closed_date`, and loans with `loan_status <> 'Closed'` but a non-NULL `closed_date`. Two numbers.",
      "SELECT COUNT(*) FILTER (WHERE loan_status='Closed' AND closed_date IS NULL), COUNT(*) FILTER (WHERE loan_status<>'Closed' AND closed_date IS NOT NULL) FROM loan"),
    P(2, "Rates keyed as fractions: in `loan_rate_history`, interest rates below 1 are probably keyed as decimals (0.0629 instead of 6.29). Count rows with `interest_rate_pct < 1`. One number.",
      "SELECT COUNT(*) FROM loan_rate_history WHERE interest_rate_pct < 1"),
    P(2, "Application status duplicates: how many (application_id, status) pairs appear more than once in `application_status_history`? One number.",
      "SELECT COUNT(*) FROM (SELECT 1 FROM application_status_history GROUP BY application_id, status HAVING COUNT(*)>1)"),
    P(2, "Missing broker on broker-channel applications: count and percentage of Broker-channel applications with NULL `broker_id` (percentage 2dp). Two numbers.",
      "SELECT COUNT(*) FILTER (WHERE broker_id IS NULL), ROUND(100.0*COUNT(*) FILTER (WHERE broker_id IS NULL)/COUNT(*),2) FROM loan_application WHERE channel='Broker'"),
    P(3, "Missing monthly snapshots (gaps): for each loan the expected number of snapshot rows equals `months on book + 1` through its last snapshot. Count loans where the number of snapshot rows differs from `MAX(months_on_book) + 1`. One number.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING COUNT(*) <> MAX(months_on_book)+1)"),
    P(3, "Find the actual missing snapshot months: for loans 1-5000, list `loan_id` and the `months_on_book` values missing between 0 and the loan's max. Use a generate_series/unnest spine. Return `loan_id`, `missing_mob`; sorted by both. (Few rows.)",
      """WITH r AS (SELECT loan_id, MAX(months_on_book) AS mx FROM loan_monthly_snapshot WHERE loan_id <= 5000 GROUP BY 1),
sp AS (SELECT loan_id, unnest(generate_series(0, mx)) AS m FROM r)
SELECT sp.loan_id, sp.m FROM sp LEFT JOIN loan_monthly_snapshot s ON s.loan_id=sp.loan_id AND s.months_on_book=sp.m WHERE s.loan_id IS NULL ORDER BY 1,2""", empty_ok=True),
    P(3, "Islands: for loan 1..N, consecutive-month arrears runs. Using gaps-and-islands on `loan_monthly_snapshot` (non-closed rows with `days_past_due >= 30`), find the longest consecutive run of 30+ DPD snapshot months for any loan. One number: `max_run`. Hint: `months_on_book - ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY months_on_book)` is constant within an island.",
      """SELECT MAX(run) FROM (SELECT loan_id, grp, COUNT(*) AS run FROM (SELECT loan_id, months_on_book - ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY months_on_book) AS grp FROM loan_monthly_snapshot WHERE days_past_due >= 30 AND loan_status <> 'Closed') GROUP BY 1,2)"""),
    P(3, "Referential integrity across tables: loan_ids in `loan_monthly_snapshot`, `loan_rate_history`, `ecl_provision_quarterly`, `loan_payment`, `hardship_arrangement`, `collections_activity`, `loan_loss` that do not exist in `loan`. Return `tbl`, `orphans` for each; sorted by `tbl`. (All expected 0.)",
      """SELECT * FROM (
SELECT 'collections_activity' AS tbl, COUNT(*) AS n FROM collections_activity WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'ecl_provision_quarterly', COUNT(*) FROM ecl_provision_quarterly WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'hardship_arrangement', COUNT(*) FROM hardship_arrangement WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_loss', COUNT(*) FROM loan_loss WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_monthly_snapshot', COUNT(*) FROM loan_monthly_snapshot WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_payment', COUNT(*) FROM loan_payment WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_rate_history', COUNT(*) FROM loan_rate_history WHERE loan_id NOT IN (SELECT loan_id FROM loan)) ORDER BY 1"""),
    P(3, "Reconcile balances: sum of `closing_balance` at 2025-12-31 for non-closed loans from the snapshot table vs sum of `ead` in `ecl_provision_quarterly` at the same date. Return `snapshot_balance`, `ecl_ead`, `difference` (0dp each). Are they the same population?",
      """SELECT ROUND(a,0), ROUND(b,0), ROUND(a-b,0) FROM (SELECT (SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed') AS a, (SELECT SUM(ead) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31') AS b)"""),
    P(3, "Impossible values: snapshot rows where `days_past_due > 0` but `arrears_amount = 0` and `hardship_flag` is false. Count. One number. (The generator says this should be 0.)",
      "SELECT COUNT(*) FROM loan_monthly_snapshot WHERE days_past_due>0 AND arrears_amount=0 AND NOT hardship_flag"),
    P(3, "Outlier hunt using the IQR rule on `original_amount`: count loans above `Q3 + 1.5*(Q3-Q1)`. One number.",
      "SELECT COUNT(*) FROM loan, (SELECT QUANTILE_CONT(original_amount,0.25) AS q1, QUANTILE_CONT(original_amount,0.75) AS q3 FROM loan) q WHERE original_amount > q.q3 + 1.5*(q.q3-q.q1)"),
    P(3, "Staleness: AVM valuations date. For each property that has at least one valuation, the age in days of its newest valuation as at 2025-12-31 - how many properties have their newest valuation older than 2 years (730 days)? One number.",
      "SELECT COUNT(*) FROM (SELECT property_id, MAX(valuation_date) AS d FROM property_valuation GROUP BY 1) WHERE DATE '2025-12-31' - d > 730"),
    P(3, "Unverified income share: per `income_type`, % of lines with NULL `verified_annual_amount` (1dp). Return `income_type`, `unverified_pct`; sorted by pct descending then type.",
      "SELECT income_type, ROUND(100.0*COUNT(*) FILTER (WHERE verified_annual_amount IS NULL)/COUNT(*),1) AS p FROM applicant_income GROUP BY 1 ORDER BY p DESC, 1"),
])
