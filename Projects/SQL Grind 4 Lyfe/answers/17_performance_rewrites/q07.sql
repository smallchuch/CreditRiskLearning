-- ============================================================================
-- 17_performance_rewrites  |  Q07  |  ★★ core
-- 
-- Naive: join all 2 million snapshot rows to `loan` before filtering. Filter the snapshot to
-- 2025-12-31 FIRST (CTE), then join, and return total balance by `purpose`. `purpose`,
-- `balance` (0dp); sorted by purpose. (Non-closed only.)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


