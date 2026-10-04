-- ============================================================================
-- 02_expressions_case_functions  |  Q19  |  ★★★ challenge
-- 
-- Compute the contractual monthly P&I repayment for loans 1-15 that are 30-year
-- (`term_months = 360`) variable loans... any loans with `term_months = 360` and `loan_id <=
-- 40`: `P*r/(1-(1+r)^-n)` with `r = interest_rate_at_origination_pct/1200` and `n =
-- term_months`, rounded to 2 dp. Return `loan_id`, `repayment`. Sorted by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 27 row(s). Sort the output as described.
-- ============================================================================


