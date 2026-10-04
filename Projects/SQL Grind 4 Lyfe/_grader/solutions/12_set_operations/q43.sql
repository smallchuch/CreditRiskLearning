SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application WHERE decision='Declined' INTERSECT SELECT primary_customer_id FROM loan)
