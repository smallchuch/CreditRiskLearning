SELECT l.loan_id, c.last_name FROM loan l JOIN customer c ON c.customer_id=l.primary_customer_id WHERE l.loan_id <= 10 ORDER BY l.loan_id
