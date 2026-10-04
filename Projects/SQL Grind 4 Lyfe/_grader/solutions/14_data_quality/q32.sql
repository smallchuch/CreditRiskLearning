SELECT COUNT(*) FROM (SELECT liability_id FROM applicant_liability GROUP BY 1 HAVING COUNT(*)>1)
