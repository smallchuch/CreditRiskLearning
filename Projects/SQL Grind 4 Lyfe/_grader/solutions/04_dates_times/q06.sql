SELECT year(origination_date) AS yr, COUNT(*) FROM loan GROUP BY 1 ORDER BY 1
