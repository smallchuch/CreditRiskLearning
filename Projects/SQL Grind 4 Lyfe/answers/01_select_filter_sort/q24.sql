-- ============================================================================
-- 01_select_filter_sort  |  Q24  |  ★★★ challenge
-- 
-- Find loans originated on a weekend. (Settlements should happen on business days.) Use
-- `strftime('%w', date)` or `dayofweek(date)` - in DuckDB `dayofweek` gives
-- 0=Sunday..6=Saturday. Return `loan_id`, `origination_date`, sorted by `loan_id`. Probably
-- 0 rows.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 925 row(s). Sort the output as described.
-- ============================================================================


