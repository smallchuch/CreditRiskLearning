SELECT COUNT(*) FROM loan c WHERE c.primary_customer_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM customer p WHERE p.customer_id=c.primary_customer_id)
