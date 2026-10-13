-- ============================================================================
-- 01_select_filter_sort  |  Q19  |  ★★ core
-- 
-- The 5 largest loans originated through the `'Broker'` channel that are still `Active`:
-- `loan_id`, `original_amount`. Largest first, ties by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 5 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, original_amount FROM loan 
WHERE loan_status = 'Active'
AND channel = 'Broker'
ORDER BY original_amount DESC
LIMIT 5;