-- ============================================================================
-- 03_nulls  |  Q18  |  ★★★ challenge
-- 
-- `NOT IN` trap. Count applications that were NOT lodged via a `'Terminated'` broker
-- (`dim_broker.status`). Applications with a NULL `broker_id` must be counted (they have no
-- terminated broker). Return one number. Write it with `NOT EXISTS`; then try `NOT IN` on
-- `broker_id` and see why it breaks.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


