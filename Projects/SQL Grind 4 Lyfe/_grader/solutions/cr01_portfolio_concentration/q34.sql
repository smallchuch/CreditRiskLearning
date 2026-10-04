SELECT COUNT(*), ROUND(SUM(closing_balance),0), ROUND(AVG(closing_balance),0), ROUND(MAX(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2019-12-31' AND loan_status<>'Closed'
