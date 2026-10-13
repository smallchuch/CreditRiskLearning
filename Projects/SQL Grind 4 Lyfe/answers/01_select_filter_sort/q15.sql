-- ============================================================================
-- 01_select_filter_sort  |  Q15  |  ★★ core
-- 
-- Applications that were approved with a policy exception AND for an amount of at least
-- $800,000. Return `application_id`, `requested_amount`, `policy_exception_reason`, sorted
-- by `requested_amount` descending then `application_id`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 76 row(s). Sort the output as described.
-- ============================================================================


SELECT application_id, requested_amount, policy_exception_reason FROM loan_application
WHERE requested_amount > 800000
AND policy_exception_reason IS NOT NULL
ORDER BY requested_amount DESC, application_id ASC;