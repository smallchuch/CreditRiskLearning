-- ============================================================================
-- cr05_origination_underwriting  |  Q05  |  ★★ core
-- 
-- Serviceability declines by policy epoch: for applications declined with code 'SERV', the
-- count per `policy_id` (range join application_date to policy). `policy_id`,
-- `serv_declines`; sorted by policy.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


