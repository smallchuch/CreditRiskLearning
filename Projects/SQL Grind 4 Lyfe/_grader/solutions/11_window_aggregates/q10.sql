SELECT snapshot_date, COUNT(*) FILTER (WHERE prev_dpd=0), COUNT(*) FILTER (WHERE prev_dpd=0 AND days_past_due>=30) FROM (
 SELECT loan_id, snapshot_date, days_past_due, loan_status, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS prev_dpd FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1
