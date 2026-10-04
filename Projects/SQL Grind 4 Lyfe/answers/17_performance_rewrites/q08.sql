-- ============================================================================
-- 17_performance_rewrites  |  Q08  |  ★★ core
-- 
-- Naive: three separate queries for approved, declined and withdrawn counts. Do it in ONE
-- pass with conditional aggregation. Return one row: `approved` (`decision = 'Approved'`),
-- `declined` (`decision = 'Declined'`), `withdrawn` (`current_status = 'Withdrawn'`).
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


