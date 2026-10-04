-- ============================================================================
-- 08_subqueries  |  Q12  |  ★★ core
-- 
-- Loans in the top-quartile of original amount (>= the 75th percentile): count them using a
-- scalar subquery `(SELECT QUANTILE_CONT(original_amount,0.75) FROM loan)`. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


