SELECT year(origination_date), COUNT(*) FROM loan GROUP BY 1 HAVING COUNT(*)>2500 ORDER BY 1
