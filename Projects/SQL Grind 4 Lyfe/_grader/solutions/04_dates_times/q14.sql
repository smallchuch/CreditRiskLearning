SELECT closure_reason, COUNT(*) FROM loan WHERE closed_date IS NOT NULL AND closed_date <= origination_date + INTERVAL 12 MONTH GROUP BY 1 ORDER BY 2 DESC, 1
