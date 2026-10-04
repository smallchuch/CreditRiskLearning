-- ============================================================================
-- 09_ctes  |  Q05  |  ★★ core
-- 
-- Monthly origination totals then month-on-month change. In a CTE build `month_start`,
-- `amount` for 2024; then in the final select return `month_start`, `amount` (0dp) and
-- `prev_amount` (0dp) using `LAG`. Sorted by `month_start`. (Previews window functions.)
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 12 row(s). Sort the output as described.
-- ============================================================================


