-- ============================================================================
-- cr03_roll_rates  |  Q06  |  ★★★ challenge
-- 
-- Full 12-month pooled roll matrix: pool all month-pairs from 2025-01-31 to 2025-12-31
-- (current month in Jan..Nov 2025 with the next row = the consecutive month-end). Return
-- `from_bucket`, `to_bucket`, `loans`, `row_pct` (1dp, share of the from-bucket); sorted by
-- from, to. Pairs only where next month's snapshot date is the next month-end.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 16 row(s). Sort the output as described.
-- ============================================================================


