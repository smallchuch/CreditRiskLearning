-- ============================================================================
-- 14_data_quality  |  Q17  |  ★★★ challenge
-- 
-- Referential integrity across tables: loan_ids in `loan_monthly_snapshot`,
-- `loan_rate_history`, `ecl_provision_quarterly`, `loan_payment`, `hardship_arrangement`,
-- `collections_activity`, `loan_loss` that do not exist in `loan`. Return `tbl`, `orphans`
-- for each; sorted by `tbl`. (All expected 0.)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 7 row(s). Sort the output as described.
-- ============================================================================


