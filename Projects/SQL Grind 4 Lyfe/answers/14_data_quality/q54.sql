-- ============================================================================
-- 14_data_quality  |  Q54  |  ★★ core
-- 
-- Orphan check: rows in `applicant_income` whose `application_id` has no match in
-- `loan_application.application_id` (ignore NULL `application_id`). Count. One number (0 =
-- clean; if not 0, why?).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


