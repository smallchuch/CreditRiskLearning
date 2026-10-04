SELECT COUNT(*) FROM (SELECT hardship_id FROM hardship_arrangement GROUP BY 1 HAVING COUNT(*)>1)
