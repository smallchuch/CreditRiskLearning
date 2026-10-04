SELECT COUNT(*) FROM loan_application c WHERE c.product_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM dim_product p WHERE p.product_id=c.product_id)
