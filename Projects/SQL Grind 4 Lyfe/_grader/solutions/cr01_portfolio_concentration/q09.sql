SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND closing_balance>1500000
