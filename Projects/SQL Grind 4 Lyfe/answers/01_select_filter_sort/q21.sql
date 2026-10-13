-- ============================================================================
-- 01_select_filter_sort  |  Q21  |  ★★★ challenge
-- 
-- Precedence trap. Loans where (`purpose` = 'Purchase - Investment' OR `purpose` =
-- 'Construction') AND `original_amount` > 1200000 AND `origination_date` >= 2024-01-01.
-- Return `loan_id`, `purpose`, `original_amount`; sorted by `loan_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 567 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, purpose, original_amount FROM loan
WHERE purpose in ('Purchase - Investment', 'Construction')
AND original_amount > 1200000
AND origination_date >= '2024-01-01'
ORDER BY loan_id;