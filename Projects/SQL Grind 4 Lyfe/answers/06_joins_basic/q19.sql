-- ============================================================================
-- 06_joins_basic  |  Q19  |  ★★★ challenge
-- 
-- Income per application: `application_income` = SUM of `COALESCE(verified, declared)`
-- across `applicant_income`. Return average per `channel` (0 dp) for applications in 2025.
-- Return `channel`, `avg_income`; sorted by `channel`. (Watch the grain: sum incomes per
-- application first, then average.)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


