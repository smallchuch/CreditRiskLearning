SELECT repayment_type, ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date = DATE '2025-12-31' AND loan_status <> 'Closed' GROUP BY 1 ORDER BY 1
