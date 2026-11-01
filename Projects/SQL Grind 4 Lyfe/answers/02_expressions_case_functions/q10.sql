-- ============================================================================
-- 02_expressions_case_functions  |  Q10  |  ★★ core
-- 
-- Customers whose surname has leading/trailing spaces (a data quality issue): return
-- `customer_id`, `last_name`, sorted by `customer_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 132 row(s). Sort the output as described.
-- ============================================================================


SELECT 
    customer_id,
    CASE
        WHEN last_name <> TRIM(last_name) THEN last_name
    END AS last_name_dq
FROM customer
WHERE last_name_dq <> 'OK'
ORDER BY customer_id ASC;
    