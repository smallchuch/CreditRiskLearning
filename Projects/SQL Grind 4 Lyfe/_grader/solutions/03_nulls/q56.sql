SELECT COUNT(*) FROM loan l JOIN loan_application a ON a.application_id=l.application_id WHERE l.branch_id IS NOT DISTINCT FROM a.branch_id
