-- ============================================================================
-- 10_window_ranking  |  Q20  |  ★★★ challenge
-- 
-- Gaps-free sequence check: loans ranked by `loan_id` - confirm `ROW_NUMBER() OVER (ORDER BY
-- loan_id)` equals `loan_id` for all loans (no gaps). Return the count of loans where they
-- differ. One number (0 means no gaps).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


