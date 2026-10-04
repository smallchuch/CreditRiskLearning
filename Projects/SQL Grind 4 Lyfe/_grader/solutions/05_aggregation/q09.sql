SELECT ROUND(SUM(interest_rate_pct*closing_balance)/SUM(closing_balance),3) FROM loan_monthly_snapshot WHERE snapshot_date = DATE '2025-12-31' AND loan_status <> 'Closed'
