WITH latest AS (SELECT loan_id, days_past_due AS d, closing_balance AS b FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
bk AS (SELECT CASE WHEN d=0 THEN 'Current' WHEN d<30 THEN '1-29' WHEN d<90 THEN '30-89' ELSE '90+' END AS bucket,
       CASE WHEN d=0 THEN 1 WHEN d<30 THEN 2 WHEN d<90 THEN 3 ELSE 4 END AS k, b FROM latest)
SELECT bucket, COUNT(*), ROUND(SUM(b),0) FROM bk GROUP BY bucket, k ORDER BY k
