-- ============================================================================
-- 02_expressions_case_functions  |  Q21  |  ★★★ challenge
-- 
-- Classify applications 1-20 into a decision-path label using nested logic: `'Exception
-- approval'` if `policy_exception_flag`; else `'Clean approval'` if `decision = 'Approved'`;
-- else `'Declined - ' || decline_reason_code` if `decision = 'Declined'`; else `'No
-- decision'`. Return `application_id`, `path`, sorted by `application_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 20 row(s). Sort the output as described.
-- ============================================================================


