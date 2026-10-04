SELECT c.customer_id, COUNT(l.loan_id) FROM customer c LEFT JOIN loan l ON l.primary_customer_id=c.customer_id WHERE c.customer_id <= 30 GROUP BY 1 ORDER BY 1
