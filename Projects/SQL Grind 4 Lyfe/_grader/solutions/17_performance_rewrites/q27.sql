SELECT COUNT(*) FROM loan l WHERE l.purpose='Equity Release / Top-up' AND EXISTS (SELECT 1 FROM loan_borrower b WHERE b.loan_id=l.loan_id AND b.borrower_role='Co-applicant')
