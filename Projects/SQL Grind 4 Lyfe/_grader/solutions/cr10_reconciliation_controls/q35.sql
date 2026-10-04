SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE channel='Branch') AS a, (SELECT COUNT(*) FROM loan_application WHERE channel='Branch' AND current_status='Settled') AS b)
