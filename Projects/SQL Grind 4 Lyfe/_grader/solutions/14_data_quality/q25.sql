SELECT COUNT(*) FROM (SELECT application_id FROM loan_application GROUP BY 1 HAVING COUNT(*)>1)
