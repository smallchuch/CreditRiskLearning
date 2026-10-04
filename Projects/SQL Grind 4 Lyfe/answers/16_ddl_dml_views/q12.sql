-- ============================================================================
-- 16_ddl_dml_views  |  Q12  |  ★★★ challenge
-- 
-- Staging pattern: build `scratch.stg_latest_snapshot` (`loan_id`, `closing_balance`,
-- `days_past_due`) for non-closed loans at 2025-12-31, then `scratch.arrears_summary` from
-- it with `bucket` ('Current','1-29','30-89','90+') and `loans`, `balance` (0dp). SELECT
-- from the summary sorted by loans descending... then bucket.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


