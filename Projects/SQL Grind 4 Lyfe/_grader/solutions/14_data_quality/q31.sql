SELECT COUNT(*) FROM (SELECT income_id FROM applicant_income GROUP BY 1 HAVING COUNT(*)>1)
