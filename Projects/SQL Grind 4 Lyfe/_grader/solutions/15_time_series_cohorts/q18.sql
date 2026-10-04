SELECT snapshot_date, COUNT(*) FILTER (WHERE days_past_due>=90 AND COALESCE(p,0)<90) FROM (SELECT snapshot_date, days_past_due, loan_status, LAG(days_past_due) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS p FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1
