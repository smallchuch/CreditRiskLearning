-- ============================================================================
-- cr09_loss_ecl  |  Q11  |  ★★★ challenge
-- 
-- Check the ECL arithmetic: count loan-quarters at 2025-12-31 where `ecl_amount` differs
-- from `ead * lgd * (pd_12m for stage 1, pd_lifetime for stage 2/3)` by more than $1. One
-- number. (Information check; may be non-zero because of model overlays.)
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


