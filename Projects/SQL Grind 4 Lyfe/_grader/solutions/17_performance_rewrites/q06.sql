SELECT COUNT(*) FROM loan l WHERE NOT EXISTS (SELECT 1 FROM hardship_arrangement h WHERE h.loan_id=l.loan_id)
