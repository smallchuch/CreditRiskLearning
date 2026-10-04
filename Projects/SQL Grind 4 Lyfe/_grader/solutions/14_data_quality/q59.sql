SELECT COUNT(*) FROM loan_event c WHERE c.loan_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM loan p WHERE p.loan_id=c.loan_id)
