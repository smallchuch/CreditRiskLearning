SELECT COUNT(*) FROM customer WHERE customer_id IN (SELECT primary_customer_id FROM loan WHERE purpose='Construction')
