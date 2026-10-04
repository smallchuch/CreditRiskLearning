-- ============================================================================
-- 17_performance_rewrites  |  Q10  |  ★★ core
-- 
-- Naive: `SELECT COUNT(DISTINCT customer_id)` via a big join. Count distinct customers who
-- have ever been 90+ DPD with a semi-join: customers (`primary_customer_id`) having a loan
-- with `EXISTS` a snapshot dpd>=90. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


