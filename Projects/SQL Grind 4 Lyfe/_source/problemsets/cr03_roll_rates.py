from . import P

PRIMER = r"""
## Scenario: roll rates - the engine of loss forecasting

A **roll-rate matrix** shows where loans in one arrears bucket are a month later.

```
                 NEXT MONTH
 THIS MONTH     Current  1-29   30-59  60-89  90+
 Current          97%     3%     0      0      0
 1-29             40%    35%    25%     0      0       <- 40% cure, 25% roll worse
 30-59            10%     5%    30%    55%     0
```

Build it with `LAG`/`LEAD`: pair each loan-month with the next month for the same loan, bucket both, count pairs.

```
 WITH m AS (SELECT loan_id, snapshot_date, bucket(dpd) AS b,
                   LEAD(bucket(dpd)) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS b_next
            FROM loan_monthly_snapshot WHERE loan_status <> 'Closed')
 SELECT b, b_next, COUNT(*) FROM m WHERE b_next IS NOT NULL GROUP BY 1,2
```
Rows should sum to 100% - divide each count by its row total with a window: `COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY b)`.

Buckets used here: `0` Current, `1` (1-29), `2` (30-59), `3` (60-89), `4` (90+).
Caveat: months where a loan closes don't have a "next" - they drop out. Missing snapshots (a planted data quirk) can fake a "next month".
"""

B = "CASE WHEN days_past_due=0 THEN 0 WHEN days_past_due<30 THEN 1 WHEN days_past_due<60 THEN 2 WHEN days_past_due<90 THEN 3 ELSE 4 END"
CONCEPT = dict(id="cr03_roll_rates", title="CR03 - Roll rates, cures and transitions", primer=PRIMER, problems=[
    P(1, "How many loan-month transitions exist for non-closed loans in 2025 (a loan with a next-month snapshot)? Use LEAD on `snapshot_date` per loan across all history; count rows where `snapshot_date` is in 2025 and a next row exists and the loan is non-closed this month. One number.",
      "SELECT COUNT(*) FROM (SELECT snapshot_date, loan_status, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS n FROM loan_monthly_snapshot) WHERE snapshot_date>=DATE '2025-01-01' AND loan_status<>'Closed' AND n IS NOT NULL"),
    P(1, f"Bucket counts at 2025-11-30 (live): bucket 0-4 using: 0 = current, 1 = 1-29, 2 = 30-59, 3 = 60-89, 4 = 90+. Return `bucket`, `loans`; sorted by bucket.",
      f"SELECT b, COUNT(*) FROM (SELECT {B} AS b FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-11-30' AND loan_status<>'Closed') GROUP BY 1 ORDER BY 1"),
    P(2, "Transition matrix counts for Nov-30-2025 -> Dec-31-2025 (non-closed in Nov, with a Dec row): `from_bucket`, `to_bucket`, `loans` using the 0-4 buckets. Sorted by from, to.",
      f"WITH m AS (SELECT loan_id, snapshot_date, {B} AS b, LEAD({B}) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS bn, loan_status, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS dn FROM loan_monthly_snapshot) SELECT b, bn, COUNT(*) FROM m WHERE snapshot_date=DATE '2025-11-30' AND dn=DATE '2025-12-31' AND loan_status<>'Closed' GROUP BY 1,2 ORDER BY 1,2"),
    P(2, "Roll rate from Current: for the 2025-11-30 -> 2025-12-31 transition, % of Current loans (bucket 0) that moved to 1-29 or worse (2dp). One number.",
      f"WITH m AS (SELECT {B} AS b, LEAD({B}) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS bn, snapshot_date, loan_status, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS dn FROM loan_monthly_snapshot) SELECT ROUND(100.0*COUNT(*) FILTER (WHERE bn>=1)/COUNT(*),2) FROM m WHERE snapshot_date=DATE '2025-11-30' AND dn=DATE '2025-12-31' AND loan_status<>'Closed' AND b=0"),
    P(2, "Cure rate: of loans in bucket 1 (1-29 DPD) at 2025-11-30 with a Dec row, the % at 0 DPD by 2025-12-31 (1dp). One number.",
      f"WITH m AS (SELECT {B} AS b, LEAD({B}) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS bn, snapshot_date, loan_status, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS dn FROM loan_monthly_snapshot) SELECT ROUND(100.0*COUNT(*) FILTER (WHERE bn=0)/COUNT(*),1) FROM m WHERE snapshot_date=DATE '2025-11-30' AND dn=DATE '2025-12-31' AND loan_status<>'Closed' AND b=1"),
    P(3, "Full 12-month pooled roll matrix: pool all month-pairs from 2025-01-31 to 2025-12-31 (current month in Jan..Nov 2025 with the next row = the consecutive month-end). Return `from_bucket`, `to_bucket`, `loans`, `row_pct` (1dp, share of the from-bucket); sorted by from, to. Pairs only where next month's snapshot date is the next month-end.",
      f"""WITH m AS (SELECT {B} AS b, LEAD({B}) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS bn, snapshot_date, loan_status, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS dn FROM loan_monthly_snapshot),
t AS (SELECT b, bn, COUNT(*) AS n FROM m WHERE snapshot_date>=DATE '2025-01-31' AND snapshot_date<DATE '2025-12-31' AND loan_status<>'Closed' AND dn=last_day(snapshot_date + INTERVAL 1 MONTH) GROUP BY 1,2)
SELECT b, bn, n, ROUND(100.0*n/SUM(n) OVER (PARTITION BY b),1) FROM t ORDER BY 1,2"""),
    P(3, "Worsening vs improving: for the pooled 2025 pairs above, the share of loan-months (all buckets) where the bucket got worse, stayed, or improved. Return `worse_pct`, `same_pct`, `better_pct` (2dp).",
      f"""WITH m AS (SELECT {B} AS b, LEAD({B}) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS bn, snapshot_date, loan_status, LEAD(snapshot_date) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS dn FROM loan_monthly_snapshot),
t AS (SELECT * FROM m WHERE snapshot_date>=DATE '2025-01-31' AND snapshot_date<DATE '2025-12-31' AND loan_status<>'Closed' AND dn=last_day(snapshot_date + INTERVAL 1 MONTH))
SELECT ROUND(100.0*COUNT(*) FILTER (WHERE bn>b)/COUNT(*),2), ROUND(100.0*COUNT(*) FILTER (WHERE bn=b)/COUNT(*),2), ROUND(100.0*COUNT(*) FILTER (WHERE bn<b)/COUNT(*),2) FROM t"""),
    P(3, "Time to cure: for loans that entered 30+ DPD in 2024 for the first time in that year (first month in 2024 with dpd >= 30 and dpd < 30 the month before), how many returned to 0 DPD within 6 months? Return `entered`, `cured_within_6m`, `cure_rate_pct` (1dp). Use snapshot months_on_book as the clock (`months_on_book` + 1 to + 6).",
      """WITH x AS (SELECT loan_id, snapshot_date, months_on_book AS mob, days_past_due AS d, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS p FROM loan_monthly_snapshot),
ent AS (SELECT loan_id, MIN(mob) AS mob FROM x WHERE snapshot_date>=DATE '2024-01-31' AND snapshot_date<=DATE '2024-12-31' AND d>=30 AND COALESCE(p,0)<30 GROUP BY 1)
SELECT COUNT(*), COUNT(*) FILTER (WHERE c.loan_id IS NOT NULL), ROUND(100.0*COUNT(*) FILTER (WHERE c.loan_id IS NOT NULL)/COUNT(*),1)
FROM ent LEFT JOIN (SELECT DISTINCT e.loan_id FROM ent e JOIN x y ON y.loan_id=e.loan_id AND y.mob BETWEEN e.mob+1 AND e.mob+6 AND y.d=0) c ON c.loan_id=ent.loan_id"""),
    P(3, "Default flow: loans whose first-ever 90+ DPD month is in each quarter of 2024 and 2025. `quarter` (label `YYYY-Qn`), `new_defaults`; sorted by quarter. Non-closed rows only for the 90+ test.",
      """SELECT year(d) || '-Q' || quarter(d), COUNT(*) FROM (SELECT loan_id, MIN(snapshot_date) AS d FROM loan_monthly_snapshot WHERE days_past_due>=90 AND loan_status<>'Closed' GROUP BY 1) WHERE d>=DATE '2024-01-01' GROUP BY 1 ORDER BY 1"""),
    P(3, "Re-default: loans that were 90+ DPD, later reached 0 DPD (cured), then went 30+ again. Count such loans. One number. Hint: self-join snapshots by loan and ordered months (e.g. three `EXISTS` with increasing `months_on_book`).",
      """SELECT COUNT(*) FROM (SELECT DISTINCT a.loan_id FROM loan_monthly_snapshot a JOIN loan_monthly_snapshot b ON b.loan_id=a.loan_id AND b.months_on_book>a.months_on_book AND b.days_past_due=0 JOIN loan_monthly_snapshot c ON c.loan_id=a.loan_id AND c.months_on_book>b.months_on_book AND c.days_past_due>=30 WHERE a.days_past_due>=90)"""),
])
