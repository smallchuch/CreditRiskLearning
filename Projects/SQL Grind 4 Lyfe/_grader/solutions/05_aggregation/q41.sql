SELECT product_id, MIN(original_amount), MAX(original_amount) FROM loan GROUP BY 1 ORDER BY 1
