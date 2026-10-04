SELECT COUNT(*) FROM (SELECT security_id FROM loan_security GROUP BY 1 HAVING COUNT(*)>1)
