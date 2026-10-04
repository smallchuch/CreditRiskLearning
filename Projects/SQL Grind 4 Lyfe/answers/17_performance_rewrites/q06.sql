-- ============================================================================
-- 17_performance_rewrites  |  Q06  |  ★★ core
-- 
-- Naive: `NOT IN (SELECT loan_id FROM hardship_arrangement)`. Rewrite with `NOT EXISTS` and
-- count loans never in hardship. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


