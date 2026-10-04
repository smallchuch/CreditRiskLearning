SELECT COUNT(*) FROM customer WHERE state='ACT' AND customer_id IN (SELECT primary_customer_id FROM loan)
