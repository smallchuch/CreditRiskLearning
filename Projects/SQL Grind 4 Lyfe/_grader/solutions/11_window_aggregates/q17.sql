SELECT loan_id, snapshot_date, ROUND(drop,0) FROM (SELECT loan_id, snapshot_date, loan_status, LAG(closing_balance) OVER (PARTITION BY loan_id ORDER BY snapshot_date)-closing_balance AS drop FROM loan_monthly_snapshot)
WHERE snapshot_date >= DATE '2025-01-01' AND loan_status<>'Closed' AND drop IS NOT NULL ORDER BY drop DESC, loan_id LIMIT 5
