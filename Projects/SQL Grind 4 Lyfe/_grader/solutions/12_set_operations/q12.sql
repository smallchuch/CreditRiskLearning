SELECT COUNT(*) FROM (SELECT loan_id FROM loan_loss UNION SELECT loan_id FROM loan WHERE loan_status='In Recovery')
