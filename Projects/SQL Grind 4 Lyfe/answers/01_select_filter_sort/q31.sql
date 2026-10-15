-- ============================================================================
-- 01_select_filter_sort  |  Q31  |  ★★ core
-- 
-- Active loans written through the `'Branch'` channel with an origination LVR above 85:
-- `loan_id`, `lvr_at_origination_pct`; highest LVR first, ties by `loan_id`; top 10.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 10 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, lvr_at_origination_pct FROM loan 
WHERE loan_status = 'Active'
AND lvr_at_origination_pct > 85
AND channel = 'Branch'
ORDER BY lvr_at_origination_pct DESC, loan_id ASC
LIMIT 10;