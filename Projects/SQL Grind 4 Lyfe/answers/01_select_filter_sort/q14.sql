-- ============================================================================
-- 01_select_filter_sort  |  Q14  |  ★★ core
-- 
-- Loans with LVR above 90% that did NOT require mortgage insurance (`lmi_flag` false) - a
-- possible data problem. Return `loan_id`, `lvr_at_origination_pct`, sorted by `loan_id`.
-- (It may return 0 rows - that is fine and the checker accepts that.)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 0 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, lvr_at_origination_pct FROM loan 
WHERE lmi_flag == 'false'
AND lvr_at_origination_pct > 90.00
ORDER BY loan_id;