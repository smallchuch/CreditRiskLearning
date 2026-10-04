-- ============================================================================
-- 11_window_aggregates  |  Q38  |  ★★★ challenge
-- 
-- Loan 1003: running count of months with `days_past_due > 0` and the highest dpd seen so
-- far (`MAX() OVER`) for its first 12 snapshots (`months_on_book` 0-11). `months_on_book`,
-- `cum_arrears_months`, `max_dpd_so_far`; sorted by months_on_book.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 12 row(s). Sort the output as described.
-- ============================================================================


