-- ============================================================================
-- 14_data_quality  |  Q43  |  ★★ core
-- 
-- Orphan check: rows in `loan` whose `product_id` has no match in `dim_product.product_id`
-- (ignore NULL `product_id`). Count. One number (0 = clean; if not 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


