-- ============================================================================
-- 14_data_quality  |  Q55  |  ★★ core
-- 
-- Orphan check: rows in `loan_security` whose `property_id` has no match in
-- `property.property_id` (ignore NULL `property_id`). Count. One number (0 = clean; if not
-- 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


