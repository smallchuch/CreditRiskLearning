SELECT COUNT(*) FROM applicant_income c WHERE c.application_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM loan_application p WHERE p.application_id=c.application_id)
