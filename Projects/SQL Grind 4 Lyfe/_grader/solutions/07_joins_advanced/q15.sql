SELECT COUNT(*) FROM credit_bureau_report b WHERE NOT EXISTS (SELECT 1 FROM application_applicant a WHERE a.application_id=b.application_id AND a.customer_id=b.customer_id)
