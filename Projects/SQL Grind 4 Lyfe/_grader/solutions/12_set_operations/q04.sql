SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application EXCEPT SELECT primary_customer_id FROM loan)
