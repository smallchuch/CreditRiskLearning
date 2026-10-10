-- ============================================================================
-- 01_select_filter_sort  |  Q01  |  ★ warm-up
-- 
-- List every product: `product_id`, `product_name`, `rate_type`. Sort by `product_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 15 row(s). Sort the output as described.
-- ============================================================================


SELECT product_id, product_name, rate_type FROM dim_product
ORDER BY product_id;