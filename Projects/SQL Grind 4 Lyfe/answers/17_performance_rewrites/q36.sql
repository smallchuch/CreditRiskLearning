-- ============================================================================
-- 17_performance_rewrites  |  Q36  |  ★★★ challenge
-- 
-- Naive: self-join for the latest status event. Use `QUALIFY ROW_NUMBER()` to get each
-- application's latest event (by ts, then event_id) and count how many of the latest events
-- are `'Settled'`... for applications 1 to 3000. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


