SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2023-06-30' AND loan_status<>'Closed'
