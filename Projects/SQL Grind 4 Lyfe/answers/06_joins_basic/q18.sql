-- ============================================================================
-- 06_joins_basic  |  Q18  |  ★★★ challenge
-- 
-- Join through the application: for approved-and-settled applications in 2025
-- (`current_status='Settled'`, `application_date` in 2025) show average bureau score (join
-- `credit_bureau_report` on application_id and customer = primary customer) per `channel`, 0
-- dp. Return `channel`, `avg_score`; sorted by `channel`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


