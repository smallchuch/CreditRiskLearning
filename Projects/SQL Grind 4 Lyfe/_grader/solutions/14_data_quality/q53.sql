SELECT COUNT(*) FROM credit_bureau_report c WHERE c.application_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM loan_application p WHERE p.application_id=c.application_id)
