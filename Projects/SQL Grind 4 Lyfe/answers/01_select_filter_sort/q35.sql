-- ============================================================================
-- 01_select_filter_sort  |  Q35  |  ★ warm-up
-- 
-- Branches in `'VIC'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 11 row(s). Sort the output as described.
-- ============================================================================


SELECT branch_id, branch_name, region FROM dim_branch
WHERE state = 'VIC'
ORDER BY branch_name ASC;