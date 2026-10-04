SELECT broker_id, COUNT(*), ROUND(SUM(original_amount),0) AS t FROM loan WHERE broker_id IS NOT NULL GROUP BY 1 HAVING COUNT(*) >= 200 ORDER BY t DESC, 1
