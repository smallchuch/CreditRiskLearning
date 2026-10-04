-- ============================================================================
-- 17_performance_rewrites  |  Q09  |  ★★ core
-- 
-- Naive: self-join to get each customer's latest application. Rewrite with `QUALIFY
-- ROW_NUMBER()`. Return the count of customers whose latest application (by date, then id)
-- was Declined. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


