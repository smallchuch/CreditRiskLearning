-- ============================================================================
-- 17_performance_rewrites  |  Q14  |  ★★★ challenge
-- 
-- Naive: window over everything then filter. Compute the top 3 largest loans per state of
-- the property efficiently: first reduce to only the columns needed, then rank. Return
-- `state`, `loan_id`, `original_amount`; sorted by state, amount descending, loan_id. Top 3
-- per state.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 24 row(s). Sort the output as described.
-- ============================================================================


