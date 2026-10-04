SELECT COUNT(DISTINCT l.loan_id) FROM loan l JOIN loan_event e ON e.loan_id=l.loan_id AND e.event_type='Retention discount applied' WHERE l.closure_reason='Refinanced to another lender'
