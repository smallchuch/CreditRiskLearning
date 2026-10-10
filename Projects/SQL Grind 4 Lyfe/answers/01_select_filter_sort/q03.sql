-- ============================================================================
-- 01_select_filter_sort  |  Q03  |  ★ warm-up
-- 
-- Show `loan_id`, `original_amount`, `origination_date` for loans with an original amount
-- over $1,500,000. Sort by amount (largest first), then `loan_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 1,778 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, original_amount, origination_date FROM loan
WHERE original_amount > 1500000
ORDER BY original_amount DESC, loan_id ASC;