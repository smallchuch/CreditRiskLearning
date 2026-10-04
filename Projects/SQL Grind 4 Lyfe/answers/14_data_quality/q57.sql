-- ============================================================================
-- 14_data_quality  |  Q57  |  ★★ core
-- 
-- Orphan check: rows in `complaint` whose `customer_id` has no match in
-- `customer.customer_id` (ignore NULL `customer_id`). Count. One number (0 = clean; if not
-- 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


