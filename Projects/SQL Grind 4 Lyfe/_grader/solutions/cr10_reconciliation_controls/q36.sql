SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE channel='Digital') AS a, (SELECT COUNT(*) FROM loan_application WHERE channel='Digital' AND current_status='Settled') AS b)
