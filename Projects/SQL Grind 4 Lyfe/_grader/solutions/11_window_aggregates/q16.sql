SELECT COUNT(*) FROM (SELECT closing_balance, interest_charged, actual_repayment, COALESCE(offset_balance,0) AS ob, LAG(closing_balance) OVER (PARTITION BY loan_id ORDER BY snapshot_date) AS pc FROM loan_monthly_snapshot WHERE loan_id <= 10)
WHERE pc IS NOT NULL AND ob=0 AND ABS(pc + interest_charged - actual_repayment - closing_balance) > 1
