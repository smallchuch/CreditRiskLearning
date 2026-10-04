SELECT product_id, ROUND(AVG(original_amount),0), ROUND(PERCENT_RANK() OVER (ORDER BY AVG(original_amount)),2) FROM loan GROUP BY 1 ORDER BY 1
