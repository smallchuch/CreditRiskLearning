-- ============================================================================
-- 01_select_filter_sort  |  Q13  |  ★★ core
-- 
-- Brokers who are not `'Active'`: `broker_id`, `firm_name`, `status`, `status_change_date`.
-- Sort by `status_change_date` (oldest first), then `broker_id`.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 61 row(s). Sort the output as described.
-- ============================================================================


SELECT broker_id, firm_name, status, status_change_date FROM dim_broker
WHERE status NOT IN ('Active')
ORDER BY status_change_date ASC;