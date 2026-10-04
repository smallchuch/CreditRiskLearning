-- ============================================================================
-- 14_data_quality  |  Q59  |  ★★ core
-- 
-- Orphan check: rows in `loan_event` whose `loan_id` has no match in `loan.loan_id` (ignore
-- NULL `loan_id`). Count. One number (0 = clean; if not 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


