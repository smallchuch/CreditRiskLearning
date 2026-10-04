WITH b AS (SELECT closing_balance AS x, NTILE(20) OVER (ORDER BY closing_balance, loan_id) AS q FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed')
SELECT COUNT(*) FILTER (WHERE q=20), ROUND(100*SUM(x) FILTER (WHERE q=20)/SUM(x),1) FROM b
