SELECT loan_id, COUNT(*), ROUND(SUM(allocated_value),0) AS t FROM loan_security GROUP BY 1 HAVING COUNT(*)>1 ORDER BY t DESC, 1 LIMIT 10
