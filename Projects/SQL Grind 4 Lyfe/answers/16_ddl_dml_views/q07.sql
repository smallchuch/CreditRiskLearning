-- ============================================================================
-- 16_ddl_dml_views  |  Q07  |  ★★ core
-- 
-- ALTER + UPDATE: create `scratch.l3` from loans 1-6 (`loan_id`, `original_amount`), ADD
-- COLUMN `size_band` VARCHAR, set it with an UPDATE to `'Large'` where amount >= 600000 else
-- `'Standard'`, then SELECT `loan_id`, `size_band` sorted by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


