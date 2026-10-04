-- ============================================================================
-- 11_window_aggregates  |  Q13  |  ★★★ challenge
-- 
-- Balance drift since the first snapshot: for loans 1-5 and their first four snapshots
-- (`months_on_book <= 4`), return `loan_id`, `months_on_book`, `closing_balance` and
-- `balance_vs_first` = closing_balance minus `FIRST_VALUE(closing_balance)` over that loan's
-- history ordered by date (2dp). Sorted by `loan_id`, `months_on_book`.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 25 row(s). Sort the output as described.
-- ============================================================================


