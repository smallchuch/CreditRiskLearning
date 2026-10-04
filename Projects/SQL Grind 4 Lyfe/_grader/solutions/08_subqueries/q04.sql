SELECT product_id, product_name FROM dim_product p WHERE NOT EXISTS (SELECT 1 FROM loan l WHERE l.product_id=p.product_id) ORDER BY 1
