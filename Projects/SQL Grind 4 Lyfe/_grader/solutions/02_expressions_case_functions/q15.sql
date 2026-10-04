SELECT product_id, ROUND(annual_fee / NULLIF(max_lvr_pct - 90, 0), 2) FROM dim_product ORDER BY product_id
