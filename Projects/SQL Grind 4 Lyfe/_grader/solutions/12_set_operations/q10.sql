SELECT COUNT(*) FROM (SELECT loan_id FROM loan WHERE loan_status='Closed' EXCEPT SELECT loan_id FROM loan_monthly_snapshot WHERE loan_status='Closed')
