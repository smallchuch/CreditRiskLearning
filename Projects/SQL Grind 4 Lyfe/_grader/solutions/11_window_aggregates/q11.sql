SELECT COUNT(*), COUNT(*) FILTER (WHERE days_past_due=0), ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due=0)/COUNT(*),1) FROM (
 SELECT days_past_due, loan_status, snapshot_date, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS prev_dpd FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' AND prev_dpd BETWEEN 30 AND 89
