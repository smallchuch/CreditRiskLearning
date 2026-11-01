-- ============================================================================
-- 02_expressions_case_functions  |  Q02  |  ★ warm-up
-- 
-- Customer full names for `customer_id` 1 to 8 in the form `First Last` (one column,
-- `full_name`), plus `customer_id`. Sorted by `customer_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 8 row(s). Sort the output as described.
-- ============================================================================


SELECT customer_id, CONCAT(first_name, ' ', last_name) AS full_name
FROM customer
ORDER BY customer_id ASC
LIMIT 8;