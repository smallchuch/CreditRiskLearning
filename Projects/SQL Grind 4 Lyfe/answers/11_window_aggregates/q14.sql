-- ============================================================================
-- 11_window_aggregates  |  Q14  |  ★★★ challenge
-- 
-- Months since last payment missed: for loan 1 compute for each snapshot a flag `shortfall`
-- = `actual_repayment < scheduled_repayment` and a running count of shortfall months
-- (`cum_shortfalls`). Return `snapshot_date`, `shortfall`, `cum_shortfalls` for loans 1,
-- snapshots on or after 2019-01-31. Sorted by date.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 22 row(s). Sort the output as described.
-- ============================================================================


