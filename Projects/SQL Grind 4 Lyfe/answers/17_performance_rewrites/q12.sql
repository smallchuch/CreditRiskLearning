-- ============================================================================
-- 17_performance_rewrites  |  Q12  |  ★★★ challenge
-- 
-- Naive: correlated `MAX` subquery to get each loan's latest snapshot. Rewrite with
-- `QUALIFY` or `arg_max`: total closing balance of every loan's LAST snapshot row for loans
-- with `loan_id <= 100`. One number (0dp).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


