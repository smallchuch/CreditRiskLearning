-- ============================================================================
-- 14_data_quality  |  Q56  |  ★★ core
-- 
-- Orphan check: rows in `property` whose `postcode` has no match in `dim_postcode.postcode`
-- (ignore NULL `postcode`). Count. One number (0 = clean; if not 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


