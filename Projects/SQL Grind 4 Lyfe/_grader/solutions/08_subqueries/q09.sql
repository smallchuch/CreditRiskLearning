SELECT product_id, MAX(origination_date) FROM loan GROUP BY 1 ORDER BY 1
