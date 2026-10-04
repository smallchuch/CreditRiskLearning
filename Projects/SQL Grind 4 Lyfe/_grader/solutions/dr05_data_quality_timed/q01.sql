SELECT COUNT(*) FROM (SELECT 1 FROM loan_application GROUP BY primary_customer_id, application_date, requested_amount HAVING COUNT(*)>1)
