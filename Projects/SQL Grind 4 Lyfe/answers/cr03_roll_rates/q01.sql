-- ============================================================================
-- cr03_roll_rates  |  Q01  |  ★ warm-up
-- 
-- How many loan-month transitions exist for non-closed loans in 2025 (a loan with a next-
-- month snapshot)? Use LEAD on `snapshot_date` per loan across all history; count rows where
-- `snapshot_date` is in 2025 and a next row exists and the loan is non-closed this month.
-- One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


