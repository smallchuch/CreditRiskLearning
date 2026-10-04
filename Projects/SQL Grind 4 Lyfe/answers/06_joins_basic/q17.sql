-- ============================================================================
-- 06_joins_basic  |  Q17  |  ★★★ challenge
-- 
-- Valuation at origination vs now: for loans 1-10 return `loan_id`,
-- `security_value_at_origination`, and the latest `valuation_amount` for the loan's property
-- from `property_valuation` with `valuation_date <= 2025-12-31` that is > 0 (AVM zeros are
-- bad data). Sorted by `loan_id`. Use a subquery or join on MAX(valuation_date).
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 10 row(s). Sort the output as described.
-- ============================================================================


