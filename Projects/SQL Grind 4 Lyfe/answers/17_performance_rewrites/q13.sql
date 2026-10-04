-- ============================================================================
-- 17_performance_rewrites  |  Q13  |  ★★★ challenge
-- 
-- Naive: functions on both sides of a join (`LOWER(a.x)=LOWER(b.x)`) are slow. Count
-- customers that share an email with another customer using GROUP BY on `LOWER(email)`
-- rather than a self-join. One number: customers whose lowercase email is shared.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


