SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2022-12-31' AND loan_status<>'Closed'
