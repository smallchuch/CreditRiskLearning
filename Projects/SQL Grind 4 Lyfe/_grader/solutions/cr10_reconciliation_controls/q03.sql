SELECT COUNT(*) FROM loan l JOIN loan_borrower b ON b.loan_id=l.loan_id AND b.borrower_role='Primary' WHERE b.customer_id<>l.primary_customer_id
