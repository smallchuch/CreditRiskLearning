SELECT ROUND(100*SUM(closing_balance) FILTER (WHERE repayment_type='Interest Only')/SUM(closing_balance),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'
