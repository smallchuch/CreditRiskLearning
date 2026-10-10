-- ============================================================================
-- 01_select_filter_sort  |  Q08  |  ★ warm-up
-- 
-- Loans with an original amount between $400,000 and $450,000 inclusive, that are still
-- `Active`. Return `loan_id`, `original_amount`, sorted by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 3,674 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, original_amount FROM loan 
WHERE loan_status = 'Active'
AND original_amount BETWEEN 400000 AND 450000
ORDER BY loan_id;