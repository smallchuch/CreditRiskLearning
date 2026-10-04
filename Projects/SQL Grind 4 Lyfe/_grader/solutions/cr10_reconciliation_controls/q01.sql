SELECT (SELECT COUNT(*) FROM loan), (SELECT COUNT(DISTINCT loan_id) FROM loan_monthly_snapshot), (SELECT COUNT(DISTINCT loan_id) FROM loan_borrower)
