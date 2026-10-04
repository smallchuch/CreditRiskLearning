SELECT CASE WHEN lvr_at_origination_pct <= 60 THEN '<=60' WHEN lvr_at_origination_pct <= 80 THEN '60-80' ELSE '>80' END AS lvr_band, COUNT(*) AS loans FROM loan GROUP BY 1 ORDER BY 2 DESC
