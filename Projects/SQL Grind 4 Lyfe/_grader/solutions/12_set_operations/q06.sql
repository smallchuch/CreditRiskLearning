SELECT COUNT(*) FROM (SELECT customer_id FROM complaint EXCEPT SELECT customer_id FROM loan_borrower)
