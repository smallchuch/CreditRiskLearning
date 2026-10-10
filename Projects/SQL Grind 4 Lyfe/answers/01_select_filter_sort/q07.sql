-- ============================================================================
-- 01_select_filter_sort  |  Q07  |  ★ warm-up
-- 
-- Loans with a fixed interest rate: return `loan_id`, `interest_rate_at_origination_pct`,
-- `fixed_rate_expiry_date` for loans originated in 2021 with `rate_type = 'Fixed'`, sorted
-- by `loan_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 3,987 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, interest_rate_at_origination_pct, fixed_rate_expiry_date FROM loan 
WHERE origination_date > '2020-12-31'
AND origination_date < '2022-01-01'
AND rate_type == 'Fixed'
ORDER BY loan_id;