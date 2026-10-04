from . import P

PRIMER = r"""
## Scenario: the monthly arrears report

Arrears = loans behind on repayments. The board sees this every month, so you must be exact and reproducible.

```
 DPD (days past due)   0     1-29     30-59    60-89    90-119   120-179   180+
 Common name        Current  Early   Past due  Past due  Default  Default   Default
                              ^ not usually reported      ^ "90+ DPD" = the regulatory default line
```

* **Arrears rate** = arrears loans / all live loans (by count) **or** arrears balance / total balance (by balance). Say which.
* `ref_arrears_bucket` gives the official bucket names (join with `days_past_due BETWEEN dpd_from AND COALESCE(dpd_to, 99999)`).
* `arrears_amount` = dollars behind; `hardship_flag` marks loans under a hardship arrangement (often excluded or reported separately).
* The **live book** = non-closed rows at the reporting snapshot.
"""

CONCEPT = dict(id="cr02_arrears_delinquency", title="CR02 - Arrears and delinquency reporting", primer=PRIMER, problems=[
    P(1, "Arrears distribution at 2025-12-31: for each official bucket (`ref_arrears_bucket`), loan count and balance (0dp). `bucket_name`, `loans`, `balance`; sorted by `bucket_id`.",
      "SELECT b.bucket_name, COUNT(*), ROUND(SUM(s.closing_balance),0) FROM loan_monthly_snapshot s JOIN ref_arrears_bucket b ON s.days_past_due BETWEEN b.dpd_from AND COALESCE(b.dpd_to,99999) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY b.bucket_id, b.bucket_name ORDER BY b.bucket_id"),
    P(1, "30+ DPD rate by count and by balance at 2025-12-31 (live book), 2dp %. Return `count_rate_pct`, `balance_rate_pct`.",
      "SELECT ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=30)/COUNT(*),2), ROUND(100*SUM(closing_balance) FILTER (WHERE days_past_due>=30)/SUM(closing_balance),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'"),
    P(1, "Total dollars in arrears (`SUM(arrears_amount)`, 0dp) on the live book at 2025-12-31, and the number of loans with arrears_amount > 0. Two numbers.",
      "SELECT ROUND(SUM(arrears_amount),0), COUNT(*) FILTER (WHERE arrears_amount>0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'"),
    P(2, "90+ DPD rate by month-end over 2025 (count basis, 2dp %), live book. `snapshot_date`, `rate_90plus_pct`; sorted by date.",
      "SELECT snapshot_date, ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=90)/COUNT(*),2) FROM loan_monthly_snapshot WHERE snapshot_date>=DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "30+ DPD rate (balance basis, 2dp) by `purpose` at 2025-12-31. `purpose`, `rate_pct`; sorted by rate descending, purpose.",
      "SELECT l.purpose, ROUND(100*SUM(s.closing_balance) FILTER (WHERE s.days_past_due>=30)/SUM(s.closing_balance),2) AS r FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY r DESC, 1"),
    P(2, "30+ DPD rate (count basis, 2dp) by `channel` at 2025-12-31. `channel`, `rate_pct`; sorted by channel.",
      "SELECT l.channel, ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Arrears by repayment type: `repayment_type`, loans, 30+ DPD loans, rate (2dp) at 2025-12-31 live book. Sorted by type.",
      "SELECT repayment_type, COUNT(*), COUNT(*) FILTER (WHERE days_past_due>=30), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Excluding hardship: 30+ DPD count at 2025-12-31 split by `hardship_flag` (true/false). `hardship_flag`, `loans_30plus`; sorted by flag.",
      "SELECT hardship_flag, COUNT(*) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due>=30 GROUP BY 1 ORDER BY 1"),
    P(2, "LVR band vs arrears: using `ref_lvr_band` on origination LVR (lower exclusive, upper inclusive, first band includes 0), the 30+ DPD rate by band (count basis, 2dp) at 2025-12-31. `band_name`, `loans`, `rate_pct`; sorted by band_id.",
      "SELECT b.band_name, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN ref_lvr_band b ON (l.lvr_at_origination_pct>b.lvr_from_pct OR b.lvr_from_pct=0) AND l.lvr_at_origination_pct<=COALESCE(b.lvr_to_pct,1e9) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY b.band_id, b.band_name ORDER BY b.band_id"),
    P(3, "Early-warning list: live loans at 2025-12-31 with `days_past_due` between 1 and 29 that were ALSO in arrears (dpd > 0) the previous month (two consecutive months). Return the count. One number.",
      "SELECT COUNT(*) FROM (SELECT snapshot_date, days_past_due, loan_status, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS p FROM loan_monthly_snapshot) WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due BETWEEN 1 AND 29 AND p>0"),
    P(3, "State league table of 90+ DPD rate (count basis, 2dp) at 2025-12-31 using property state. Show only states with at least 1,000 live loans. `state`, `live_loans`, `rate_90plus_pct`; sorted by rate descending then state.",
      "SELECT d.state, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=90)/COUNT(*),2) AS r FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 HAVING COUNT(*)>=1000 ORDER BY r DESC, 1"),
    P(3, "Origination-year arrears: for each origination year, 30+ DPD rate (count, 2dp) at 2025-12-31 on live loans. `yr`, `live_loans`, `rate_pct`; sorted by year.",
      "SELECT year(l.origination_date), COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE s.days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(3, "Months in arrears distribution: for live loans at 2025-12-31 with dpd >= 30 now, how many snapshots (months) in the last 12 (`snapshot_date > 2024-12-31`) had dpd >= 30? Return `months_30plus`, `loans`; sorted by months.",
      """WITH now AS (SELECT loan_id FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due>=30)
SELECT n, COUNT(*) FROM (SELECT s.loan_id, COUNT(*) FILTER (WHERE s.days_past_due>=30) AS n FROM loan_monthly_snapshot s JOIN now USING (loan_id) WHERE s.snapshot_date > DATE '2024-12-31' GROUP BY 1) GROUP BY 1 ORDER BY 1"""),
    P(3, "Reconcile arrears dollars to days: loans at 2025-12-31 (live) with `days_past_due >= 30` but `arrears_amount` below one scheduled repayment (`arrears_amount < scheduled_repayment`) - potential data issue. Count them. One number.",
      "SELECT COUNT(*) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due>=30 AND arrears_amount < scheduled_repayment"),
])
