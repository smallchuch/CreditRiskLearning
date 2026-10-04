SELECT product_id FROM dim_product WHERE product_id <= 3 UNION SELECT product_id FROM dim_product WHERE product_id BETWEEN 3 AND 5 ORDER BY 1
