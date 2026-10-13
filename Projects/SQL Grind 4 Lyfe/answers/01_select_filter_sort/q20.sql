-- ============================================================================
-- 01_select_filter_sort  |  Q20  |  ★★★ challenge
-- 
-- Applications that are 'in flight' at the snapshot date: `current_status` is `'In
-- Progress'` or `'Approved - Awaiting Settlement'`, AND the application was lodged on or
-- after 2025-12-01. Return `application_id`, `application_date`, `current_status`, sorted by
-- `application_date`, `application_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 1,933 row(s). Sort the output as described.
-- ============================================================================


SELECT application_id, application_date, current_status FROM loan_application
WHERE current_status IN ('In Progress', 'Approved - Awaiting Settlement')
AND application_date >= '2025-12-01'
ORDER BY application_date ASC, application_id ASC;