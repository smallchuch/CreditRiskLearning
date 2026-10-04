-- ============================================================================
-- 11_window_aggregates  |  Q16  |  ★★★ challenge
-- 
-- Closing-balance reconciliation. For loans 1-10 and their snapshots, check balance
-- continuity: `prev_close + interest_charged - actual_repayment` should be close to
-- `closing_balance` (within $1 after allowing for offset effects - treat only loans with
-- `offset_balance` = 0 or NULL). Count the snapshot rows where the difference exceeds $1.
-- One number (information only).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


