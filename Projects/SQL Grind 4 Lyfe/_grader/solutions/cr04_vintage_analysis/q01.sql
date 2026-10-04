SELECT year(origination_date), COUNT(*), ROUND(AVG(original_amount),0) FROM loan GROUP BY 1 ORDER BY 1
