-- ============================================================================
-- 17_performance_rewrites  |  Q35  |  ★★ core
-- 
-- Naive: join all snapshot rows then filter. Filter the snapshot to 2025-12-31 first, then
-- join: live balance (0 dp) by `channel`. `channel`, `balance`; sorted by channel.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


