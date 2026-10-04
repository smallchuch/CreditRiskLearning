from . import P

PRIMER = r"""
## GROUP BY = fold many rows into one row per group

```
 loan rows                          GROUP BY purpose                result
 purpose     amount                 +-----------------------+
 Refinance   500k   --+            | Refinance  : 500,700   |      purpose     n   total
 Refinance   700k   --+--> bucket  +-----------------------+      Refinance   2   1.2m
 Construct.  300k   ----> bucket   | Construct. : 300       |      Construct.  1   0.3m
```

| Function | Meaning | NULLs |
|---|---|---|
| `COUNT(*)` | rows | counts all |
| `COUNT(x)` | non-NULL x | skips |
| `COUNT(DISTINCT x)` | unique x | skips |
| `SUM/AVG/MIN/MAX` | as named | skip |
| `COUNT(*) FILTER (WHERE cond)` | conditional count | - |
| `MEDIAN(x)`, `QUANTILE_CONT(x, 0.9)` | statistics | skip |

**WHERE vs HAVING**: `WHERE` filters rows *before* grouping; `HAVING` filters groups *after*.

```
 FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

**Rule:** every column in `SELECT` must be either in `GROUP BY` or inside an aggregate.
`GROUP BY ALL` (DuckDB) groups by all non-aggregated select columns - great for quick work.

**Weighted average** (credit risk staple): `SUM(x*w)/SUM(w)`, e.g. balance-weighted rate = `SUM(rate*balance)/SUM(balance)`.
"""

CONCEPT = dict(id="05_aggregation", title="05 - Aggregation: GROUP BY, HAVING, conditional aggregates", primer=PRIMER, problems=[
    P(1, "Total original lending: `SUM(original_amount)` across all loans, rounded to 0 dp.",
      "SELECT ROUND(SUM(original_amount),0) FROM loan"),
    P(1, "Number of loans per `purpose`. Return `purpose`, `loans`; sorted by `loans` descending then `purpose`.",
      "SELECT purpose, COUNT(*) FROM loan GROUP BY 1 ORDER BY 2 DESC, 1"),
    P(1, "Average original loan amount per `channel`, rounded to 0 dp. Return `channel`, `avg_amount`; sorted by `channel`.",
      "SELECT channel, ROUND(AVG(original_amount),0) FROM loan GROUP BY 1 ORDER BY 1"),
    P(1, "Number of distinct primary customers with a loan. One number.",
      "SELECT COUNT(DISTINCT primary_customer_id) FROM loan"),
    P(1, "Smallest, largest and average `original_amount` for Active loans (average rounded to 0 dp). Three columns: min, max, avg.",
      "SELECT MIN(original_amount), MAX(original_amount), ROUND(AVG(original_amount),0) FROM loan WHERE loan_status='Active'"),
    P(1, "Loans per `loan_status`. Return `loan_status`, `loans`; sorted by `loan_status`.",
      "SELECT loan_status, COUNT(*) FROM loan GROUP BY 1 ORDER BY 1"),
    P(2, "For each origination year and `purpose`: number of loans. Return `yr`, `purpose`, `loans`; sorted by `yr`, `purpose`.",
      "SELECT year(origination_date), purpose, COUNT(*) FROM loan GROUP BY 1,2 ORDER BY 1,2"),
    P(2, "Which `product_id` values have more than 3,000 loans? Return `product_id`, `loans`; sorted by `product_id`.",
      "SELECT product_id, COUNT(*) FROM loan GROUP BY 1 HAVING COUNT(*) > 3000 ORDER BY 1"),
    P(2, "Balance-weighted average interest rate on the latest snapshot (`snapshot_date = 2025-12-31`) for non-closed loans, as a single number rounded to 3 dp: `SUM(rate*balance)/SUM(balance)`. Use `closing_balance` and `interest_rate_pct`.",
      "SELECT ROUND(SUM(interest_rate_pct*closing_balance)/SUM(closing_balance),3) FROM loan_monthly_snapshot WHERE snapshot_date = DATE '2025-12-31' AND loan_status <> 'Closed'"),
    P(2, "Total outstanding balance at 2025-12-31 by `repayment_type` for non-closed loans. Return `repayment_type`, `balance` (0 dp); sorted by `repayment_type`.",
      "SELECT repayment_type, ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date = DATE '2025-12-31' AND loan_status <> 'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Approval rate by `channel` for applications that reached a decision: `Approved` count / decided count, as a % to 1 dp. Return `channel`, `approval_pct`; sorted by `channel`.",
      "SELECT channel, ROUND(100.0*COUNT(*) FILTER (WHERE decision='Approved')/COUNT(decision),1) FROM loan_application GROUP BY 1 ORDER BY 1"),
    P(2, "Number of applications per `decline_reason_code` (declined only, code not null). Return `decline_reason_code`, `n`; sorted by `n` descending, then code.",
      "SELECT decline_reason_code, COUNT(*) FROM loan_application WHERE decision='Declined' AND decline_reason_code IS NOT NULL GROUP BY 1 ORDER BY 2 DESC, 1"),
    P(2, "Per `broker_id` (not NULL): number of loans and total original amount (0 dp). Show only brokers with at least 200 loans. Return `broker_id`, `loans`, `total_amount`; sorted by `total_amount` descending then `broker_id`.",
      "SELECT broker_id, COUNT(*), ROUND(SUM(original_amount),0) AS t FROM loan WHERE broker_id IS NOT NULL GROUP BY 1 HAVING COUNT(*) >= 200 ORDER BY t DESC, 1"),
    P(2, "Average LVR at origination per `purpose` (1 dp), excluding Internal Refinance. Return `purpose`, `avg_lvr`; sorted by `purpose`.",
      "SELECT purpose, ROUND(AVG(lvr_at_origination_pct),1) FROM loan WHERE purpose <> 'Internal Refinance' GROUP BY 1 ORDER BY 1"),
    P(2, "Use `GROUP BY ALL`: count loans by `rate_type`, `loan_status`. Return `rate_type`, `loan_status`, `loans`; sorted by the first two.",
      "SELECT rate_type, loan_status, COUNT(*) AS loans FROM loan GROUP BY ALL ORDER BY 1,2"),
    P(2, "One-row portfolio summary of Active loans at 2025-12-31 (snapshot table): `loan_count`, `total_balance` (0dp), `avg_balance` (0dp), `max_balance` (0dp).",
      "SELECT COUNT(*), ROUND(SUM(closing_balance),0), ROUND(AVG(closing_balance),0), ROUND(MAX(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date = DATE '2025-12-31' AND loan_status='Active'"),
    P(3, "Conditional aggregation in one pass: for each `channel`, return counts of loans in each LVR bucket: `lvr_le80` (<= 80), `lvr_80_90` (> 80 and <= 90), `lvr_gt90` (> 90). Return `channel`, those three counts; sorted by `channel`.",
      "SELECT channel, COUNT(*) FILTER (WHERE lvr_at_origination_pct <= 80), COUNT(*) FILTER (WHERE lvr_at_origination_pct > 80 AND lvr_at_origination_pct <= 90), COUNT(*) FILTER (WHERE lvr_at_origination_pct > 90) FROM loan GROUP BY 1 ORDER BY 1"),
    P(3, "Arrears rate. At 2025-12-31, for non-closed loans: `loans`, `loans_30plus` (days_past_due >= 30), `loans_90plus` (>= 90), and the 90+ rate as % of balance (2 dp) = SUM(balance where dpd>=90)/SUM(balance)*100. Return the four values as one row: loans, loans_30plus, loans_90plus, pct_balance_90plus.",
      "SELECT COUNT(*), COUNT(*) FILTER (WHERE days_past_due>=30), COUNT(*) FILTER (WHERE days_past_due>=90), ROUND(100*SUM(closing_balance) FILTER (WHERE days_past_due>=90)/SUM(closing_balance),2) FROM loan_monthly_snapshot WHERE snapshot_date = DATE '2025-12-31' AND loan_status <> 'Closed'"),
    P(3, "Median vs mean. For loans originated in 2025 compute, per `purpose`, the average and the median `original_amount` (both 0 dp). Return `purpose`, `avg_amount`, `median_amount`; sorted by `purpose`.",
      "SELECT purpose, ROUND(AVG(original_amount),0), ROUND(MEDIAN(original_amount),0) FROM loan WHERE origination_date >= DATE '2025-01-01' GROUP BY 1 ORDER BY 1"),
    P(3, "Concentration: share of total Active-loan balance (snapshot 2025-12-31) held by each state of the property postcode. Join snapshot -> loan -> property -> dim_postcode. Return `state`, `balance_share_pct` (1 dp); sorted by share descending then `state`.",
      """SELECT p.state, ROUND(100.0*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) AS sh
FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property pr ON pr.property_id=l.property_id JOIN dim_postcode p ON p.postcode=pr.postcode
WHERE s.snapshot_date = DATE '2025-12-31' AND s.loan_status='Active' GROUP BY 1 ORDER BY sh DESC, 1"""),
    P(3, "Customers with the most loans. Return `primary_customer_id`, `loans` for customers with 4 or more loans as primary; sorted by `loans` descending then id. (Counts include closed and internal-refinance child loans.)",
      "SELECT primary_customer_id, COUNT(*) AS n FROM loan GROUP BY 1 HAVING COUNT(*) >= 4 ORDER BY n DESC, 1"),
    P(3, "Fixed vs variable pricing check: per `rate_type` and origination year, the average `interest_rate_at_origination_pct` (2 dp). Return `rate_type`, `yr`, `avg_rate`; sorted by `rate_type`, `yr`.",
      "SELECT rate_type, year(origination_date), ROUND(AVG(interest_rate_at_origination_pct),2) FROM loan GROUP BY 1,2 ORDER BY 1,2"),
    P(3, "Spot the HAVING-vs-WHERE difference: states (from `customer.state` after UPPER/TRIM) where the share of customers with a NULL DOB exceeds 0.17% - return `state_clean`, `null_dob`, `customers`, `pct` (2dp) for those states, sorted by `state_clean`. Only keep rows where state_clean is a clean 2-3 letter code.",
      """SELECT s, COUNT(*) FILTER (WHERE date_of_birth IS NULL) AS nd, COUNT(*) AS c, ROUND(100.0*COUNT(*) FILTER (WHERE date_of_birth IS NULL)/COUNT(*),2) AS pct
FROM (SELECT UPPER(TRIM(state)) AS s, date_of_birth FROM customer) WHERE LENGTH(s) <= 3 AND REPLACE(s,'.','')=s GROUP BY s HAVING 100.0*COUNT(*) FILTER (WHERE date_of_birth IS NULL)/COUNT(*) > 0.17 ORDER BY s"""),
])
