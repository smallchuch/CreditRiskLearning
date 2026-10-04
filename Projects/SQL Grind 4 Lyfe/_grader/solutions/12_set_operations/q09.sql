SELECT COUNT(*) FROM (SELECT loan_id FROM loan EXCEPT SELECT loan_id FROM loan_monthly_snapshot)
