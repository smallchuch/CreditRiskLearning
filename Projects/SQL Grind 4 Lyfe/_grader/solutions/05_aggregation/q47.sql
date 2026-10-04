SELECT year(origination_date), ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER (),1) FROM loan GROUP BY 1 ORDER BY 1
