-- ============================================================================
-- 01_select_filter_sort  |  Q22  |  ★★★ challenge
-- 
-- Staff who have left the bank: `staff_id`, `full_name`, `team`, `termination_date` where
-- `termination_date` is not null and falls in calendar year 2024. Sorted by
-- `termination_date`, `staff_id`.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 3 row(s). Sort the output as described.
-- ============================================================================


SELECT staff_id, full_name, team, termination_date FROM dim_staff
WHERE termination_date IS NOT NULL
AND termination_date BETWEEN '2024-01-01' AND '2025-01-01'
ORDER BY termination_date ASC, staff_id ASC;