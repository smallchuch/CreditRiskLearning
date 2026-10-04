SELECT COUNT(*) FROM loan l JOIN (SELECT loan_id, SUM(allocated_value) AS v FROM loan_security GROUP BY 1) s USING (loan_id) WHERE ABS(l.security_value_at_origination - s.v) > 1
