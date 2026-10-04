SELECT year(origination_date), purpose, COUNT(*) FROM loan GROUP BY 1,2 ORDER BY 1,2
