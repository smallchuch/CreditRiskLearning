-- ============================================================================
-- 01_select_filter_sort  |  Q12  |  ★★ core
-- 
-- Loans that are NOT owner-occupied-purchase and NOT refinance: return `loan_id`, `purpose`
-- for purposes other than `'Purchase - Owner Occupied'` and `'Refinance'` that originated in
-- December 2025. Sorted by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 650 row(s). Sort the output as described.
-- ============================================================================

SELECT loan_id, purpose FROM loan 
WHERE purpose NOT IN ('Purchase - Owner Occupied', 'Refinance')
AND origination_date BETWEEN '2025-12-01' AND '2025-12-31'
ORDER BY loan_id;
