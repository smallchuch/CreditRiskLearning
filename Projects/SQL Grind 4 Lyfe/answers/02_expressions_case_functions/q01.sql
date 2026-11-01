-- ============================================================================
-- 02_expressions_case_functions  |  Q01  |  ★ warm-up
-- 
-- For loans 1 to 10 return `loan_id` and the simple principal per month: `original_amount /
-- term_months` rounded to 2 decimals. Sorted by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 10 row(s). Sort the output as described.
-- ============================================================================

SELECT loan_id, ROUND(original_amount / term_months, 2) AS simple_principal
FROM loan 
ORDER BY loan_id ASC
LIMIT 10;
