-- ============================================================================
-- 01_select_filter_sort  |  Q37  |  ★ warm-up
-- 
-- Branches in `'SA'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 18 row(s). Sort the output as described.
-- ============================================================================


SELECT branch_id, branch_name, region FROM dim_branch
WHERE state = 'SA'
ORDER BY branch_name ASC;