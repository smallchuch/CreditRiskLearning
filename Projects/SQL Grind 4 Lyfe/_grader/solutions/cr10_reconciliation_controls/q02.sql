SELECT COUNT(*) FROM (SELECT loan_id FROM loan_borrower WHERE borrower_role='Primary' GROUP BY 1 HAVING COUNT(*)<>1) a
