-- ============================================================================
-- 06_joins_basic  |  Q13  |  ★★ core
-- 
-- Arrears bucket labels. Using `ref_arrears_bucket` joined on `days_past_due BETWEEN
-- dpd_from AND COALESCE(dpd_to, 99999)` count non-closed loans at 2025-12-31 per
-- `bucket_name`. Return `bucket_name`, `loans`; sorted by `bucket_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 7 row(s). Sort the output as described.
-- ============================================================================


