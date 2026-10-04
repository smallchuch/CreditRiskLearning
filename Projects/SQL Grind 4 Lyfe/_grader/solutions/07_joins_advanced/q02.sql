SELECT COUNT(*) FROM loan_application a WHERE EXISTS (SELECT 1 FROM loan l WHERE l.application_id=a.application_id)
