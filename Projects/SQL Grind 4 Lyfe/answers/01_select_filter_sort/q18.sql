-- ============================================================================
-- 01_select_filter_sort  |  Q18  |  ★★ core
-- 
-- Distinct combinations that exist in `dim_product`: return the three columns (`rate_type`,
-- `repayment_type`, `occupancy`) sorted by all three.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


SELECT DISTINCT rate_type, repayment_type, occupancy FROM dim_product
ORDER BY rate_type ASC, repayment_type ASC, occupancy ASC;
