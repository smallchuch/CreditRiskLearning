SELECT COUNT(*) FROM customer WHERE state='WA' AND customer_id IN (SELECT primary_customer_id FROM loan)
