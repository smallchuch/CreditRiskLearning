SELECT COUNT(*) FROM (SELECT loan_id FROM loan WHERE closure_reason='Refinanced to another lender' EXCEPT SELECT loan_id FROM loan_event WHERE event_type='Retention discount applied')
