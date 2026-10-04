SELECT loan_id, COUNT(*) FROM loan_security GROUP BY 1 HAVING COUNT(*) > 1 ORDER BY 1
