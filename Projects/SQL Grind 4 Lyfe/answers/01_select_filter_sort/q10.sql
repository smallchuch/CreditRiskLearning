-- ============================================================================
-- 01_select_filter_sort  |  Q10  |  ★★ core
-- 
-- Customers whose surname starts with `Mc`. Return `customer_id`, `first_name`, `last_name`
-- sorted by `last_name`, `first_name`, `customer_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 665 row(s). Sort the output as described.
-- ============================================================================


SELECT customer_id, first_name, last_name FROM customer

WHERE LEFT(last_name, 2) = 'Mc'

ORDER BY last_name, first_name, customer_id;