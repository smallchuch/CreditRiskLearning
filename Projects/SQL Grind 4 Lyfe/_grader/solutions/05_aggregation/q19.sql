SELECT purpose, ROUND(AVG(original_amount),0), ROUND(MEDIAN(original_amount),0) FROM loan WHERE origination_date >= DATE '2025-01-01' GROUP BY 1 ORDER BY 1
