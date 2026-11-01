-- ============================================================================
-- 01_select_filter_sort  |  Q56  |  ★★ core
-- 
-- Applications lodged in 2025 with `current_status = 'Approved - Awaiting Settlement'` and a
-- requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties
-- by `application_id`; top 10.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 10 row(s). Sort the output as described.
-- ============================================================================



SELECT application_id, requested_amount FROM loan_application
WHERE current_status = 'Approved - Awaiting Settlement'
AND requested_amount > 400000
AND application_date BETWEEN '2024-12-31' AND '2025-12-31'
ORDER BY requested_amount DESC, application_id ASC
LIMIT 10;