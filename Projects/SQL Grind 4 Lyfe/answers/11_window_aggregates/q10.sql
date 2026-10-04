-- ============================================================================
-- 11_window_aggregates  |  Q10  |  ★★★ challenge
-- 
-- Roll-rate seed. For each month-end in 2025, using LAG per loan, count loans that were 0
-- DPD last month and 30+ DPD this month (`rolled_to_30plus`) and loans that were 0 DPD last
-- month (`from_current`). Return `snapshot_date`, `from_current`, `rolled_to_30plus`; sorted
-- by `snapshot_date`. Only snapshot dates in 2025; non-closed loans.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 12 row(s). Sort the output as described.
-- ============================================================================


