-- ============================================================================
-- 01_select_filter_sort  |  Q46  |  ★★ core
-- 
-- The 5 loans with the highest `interest_rate_at_origination_pct` originated in 2021:
-- `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 5 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, interest_rate_at_origination_pct FROM loan 
WHERE origination_date BETWEEN '2020-12-31' AND '2021-12-31'
ORDER BY interest_rate_at_origination_pct DESC, loan_id ASC
LIMIT 5;
