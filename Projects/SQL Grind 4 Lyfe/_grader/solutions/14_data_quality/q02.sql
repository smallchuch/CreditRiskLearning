SELECT COUNT(*) FROM loan l WHERE NOT EXISTS (SELECT 1 FROM dim_product p WHERE p.product_id=l.product_id)
