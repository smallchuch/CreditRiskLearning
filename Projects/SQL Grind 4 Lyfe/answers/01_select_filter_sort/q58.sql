-- ============================================================================
-- 01_select_filter_sort  |  Q58  |  ★★★ challenge
-- 
-- Distinct combinations of `channel` and `purpose` for loans originated in 2025: sorted by
-- `channel`, `purpose`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 21 row(s). Sort the output as described.
-- ============================================================================


SELECT DISTINCT channel, purpose 
FROM loan 
WHERE EXTRACT(YEAR FROM origination_date) = 2025
ORDER BY channel ASC, purpose ASC;