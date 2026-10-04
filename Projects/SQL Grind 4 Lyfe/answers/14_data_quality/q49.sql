-- ============================================================================
-- 14_data_quality  |  Q49  |  ★★ core
-- 
-- Orphan check: rows in `loan_application` whose `assessor_staff_id` has no match in
-- `dim_staff.staff_id` (ignore NULL `assessor_staff_id`). Count. One number (0 = clean; if
-- not 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


