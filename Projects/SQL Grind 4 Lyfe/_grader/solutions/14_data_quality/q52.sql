SELECT COUNT(*) FROM application_applicant c WHERE c.customer_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM customer p WHERE p.customer_id=c.customer_id)
