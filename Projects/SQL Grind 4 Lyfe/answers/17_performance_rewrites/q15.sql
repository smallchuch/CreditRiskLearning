-- ============================================================================
-- 17_performance_rewrites  |  Q15  |  ★★★ challenge
-- 
-- Naive: count how many loans had a 30+ DPD month by scanning with `IN (SELECT ...)`.
-- Rewrite as an aggregate over the snapshot then count. One number: loans with
-- `MAX(days_past_due) >= 30`.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


