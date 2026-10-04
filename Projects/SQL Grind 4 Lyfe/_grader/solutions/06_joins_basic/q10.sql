SELECT l.loan_id, a.requested_amount, l.original_amount FROM loan l JOIN loan_application a ON a.application_id=l.application_id WHERE l.loan_id <= 10 ORDER BY l.loan_id
