SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE channel='Broker') AS a, (SELECT COUNT(*) FROM loan_application WHERE channel='Broker' AND current_status='Settled') AS b)
