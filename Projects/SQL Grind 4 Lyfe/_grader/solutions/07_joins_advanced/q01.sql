SELECT COUNT(*) FROM customer c WHERE NOT EXISTS (SELECT 1 FROM loan l WHERE l.primary_customer_id=c.customer_id)
