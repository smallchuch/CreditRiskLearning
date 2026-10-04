SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application UNION SELECT customer_id FROM application_applicant)
