SELECT c.loan_id, p.loan_id, p.closed_date, c.origination_date FROM loan c JOIN loan p ON p.loan_id=c.parent_loan_id ORDER BY c.loan_id LIMIT 10
