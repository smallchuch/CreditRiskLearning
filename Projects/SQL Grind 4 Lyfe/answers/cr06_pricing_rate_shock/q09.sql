-- ============================================================================
-- cr06_pricing_rate_shock  |  Q09  |  ★★★ challenge
-- 
-- IO conversion shock: loans that converted IO -> P&I in 2025 (event 'Interest-only period
-- ended - converted to P&I' in 2025). Average scheduled repayment the month BEFORE and the
-- month AFTER the event month, using the snapshots (the event month's `snapshot_date` =
-- last_day(event_date)). `loans`, `avg_before`, `avg_after`, `increase_pct` (all 1dp except
-- loans). Pairs where both snapshots exist.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


