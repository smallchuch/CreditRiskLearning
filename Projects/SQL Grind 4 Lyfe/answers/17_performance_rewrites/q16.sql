-- ============================================================================
-- 17_performance_rewrites  |  Q16  |  ★★★ challenge
-- 
-- Naive: join `loan_payment` (900k rows) to everything. Aggregate payments first: per
-- `payment_status`, count and total (0dp) of payments made in the last 3 months to
-- 2025-12-31 (`payment_date > 2025-09-30`). `payment_status`, `n`, `total`; sorted by
-- status.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 2 row(s). Sort the output as described.
-- ============================================================================


