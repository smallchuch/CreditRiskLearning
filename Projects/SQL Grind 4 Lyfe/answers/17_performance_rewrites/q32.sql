-- ============================================================================
-- 17_performance_rewrites  |  Q32  |  ★★ core
-- 
-- Naive: correlated subquery per row to get each customer's loan count. Rewrite with a pre-
-- aggregation: customers with 3 or more loans via `'Mobile Lender'`. Count. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


