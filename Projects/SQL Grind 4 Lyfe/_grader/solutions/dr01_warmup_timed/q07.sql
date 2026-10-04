SELECT broker_id, COUNT(*) AS n, ROUND(AVG(lvr_at_origination_pct),1) FROM loan WHERE broker_id IS NOT NULL GROUP BY 1 HAVING COUNT(*)>100 AND AVG(lvr_at_origination_pct)>70 ORDER BY n DESC, 1
