-- ============================================================================
-- 01_select_filter_sort  |  Q27  |  ★ warm-up
-- 
-- Loans with purpose `'Refinance'` originated in 2023 with an original amount over $500,000:
-- return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 10 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, original_amount FROM loan 
WHERE purpose ='Refinance'
AND origination_date BETWEEN '2022-12-31' AND '2023-12-31'
AND original_amount > 500000
ORDER BY original_amount DESC, loan_id ASC
LIMIT 10;