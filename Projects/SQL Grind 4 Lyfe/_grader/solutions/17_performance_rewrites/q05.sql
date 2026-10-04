SELECT COUNT(*) FROM loan l WHERE EXISTS (SELECT 1 FROM loan_borrower b WHERE b.loan_id=l.loan_id AND b.borrower_role='Co-applicant')
