SELECT broker_id, ROUND(t,0) FROM (SELECT broker_id, SUM(original_amount) AS t FROM loan WHERE broker_id IS NOT NULL GROUP BY 1)
WHERE t > (SELECT AVG(t2) FROM (SELECT SUM(original_amount) AS t2 FROM loan WHERE broker_id IS NOT NULL GROUP BY broker_id)) ORDER BY t DESC, 1
