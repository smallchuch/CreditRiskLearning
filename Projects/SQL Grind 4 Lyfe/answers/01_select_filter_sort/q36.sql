-- ============================================================================
-- 01_select_filter_sort  |  Q36  |  ★ warm-up
-- 
-- Branches in `'QLD'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 7 row(s). Sort the output as described.
-- ============================================================================


SELECT branch_id, branch_name, region FROM dim_branch
WHERE state = 'QLD'
ORDER BY branch_name ASC;