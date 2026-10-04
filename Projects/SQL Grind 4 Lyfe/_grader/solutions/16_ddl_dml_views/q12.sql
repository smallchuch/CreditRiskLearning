CREATE OR REPLACE TABLE scratch.stg_latest_snapshot AS SELECT loan_id, closing_balance, days_past_due FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed';
CREATE OR REPLACE TABLE scratch.arrears_summary AS SELECT CASE WHEN days_past_due=0 THEN 'Current' WHEN days_past_due<30 THEN '1-29' WHEN days_past_due<90 THEN '30-89' ELSE '90+' END AS bucket, COUNT(*) AS loans, ROUND(SUM(closing_balance),0) AS balance FROM scratch.stg_latest_snapshot GROUP BY 1;
SELECT bucket, loans, balance FROM scratch.arrears_summary ORDER BY loans DESC, bucket
