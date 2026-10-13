-- ============================================================================
-- 01_select_filter_sort  |  Q09  |  ★★ core
-- 
-- Applications for either `'Construction'` or `'Equity Release / Top-up'` purposes that were
-- `Declined`. Return `application_id`, `purpose`, `decline_reason_code`; sorted by
-- `application_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 4,222 row(s). Sort the output as described.
-- ============================================================================


SELECT  application_id, purpose, decline_reason_code FROM loan_application 
WHERE purpose IN ('Construction', 'Equity Release / Top-up')
AND decision == 'Declined'
ORDER BY application_id;