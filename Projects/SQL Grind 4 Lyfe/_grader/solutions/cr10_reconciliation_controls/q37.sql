SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE channel='Mobile Lender') AS a, (SELECT COUNT(*) FROM loan_application WHERE channel='Mobile Lender' AND current_status='Settled') AS b)
