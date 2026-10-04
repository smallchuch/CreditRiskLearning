-- ============================================================================
-- 11_window_aggregates  |  Q05  |  ★★ core
-- 
-- 3-month moving average of loans originated per month, for all months in 2025:
-- `month_start`, `loans`, `ma3` (1dp) using `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` over
-- the full monthly series (so January 2025 uses Nov-Dec 2024 as well). Return only 2025
-- months, sorted.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 12 row(s). Sort the output as described.
-- ============================================================================


