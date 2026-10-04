SELECT year(origination_date), COUNT(*), ROUND(SUM(original_amount),0) FROM loan GROUP BY 1 ORDER BY 1
