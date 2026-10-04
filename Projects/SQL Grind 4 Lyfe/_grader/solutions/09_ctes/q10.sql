WITH bal AS (SELECT loan_id, closing_balance AS b FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),
top AS (SELECT b FROM bal ORDER BY b DESC, loan_id LIMIT 100)
SELECT ROUND(100.0*(SELECT SUM(b) FROM top)/(SELECT SUM(b) FROM bal),2)
