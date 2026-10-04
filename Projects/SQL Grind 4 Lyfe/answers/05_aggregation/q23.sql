-- ============================================================================
-- 05_aggregation  |  Q23  |  ★★★ challenge
-- 
-- Spot the HAVING-vs-WHERE difference: states (from `customer.state` after UPPER/TRIM) where
-- the share of customers with a NULL DOB exceeds 0.17% - return `state_clean`, `null_dob`,
-- `customers`, `pct` (2dp) for those states, sorted by `state_clean`. Only keep rows where
-- state_clean is a clean 2-3 letter code.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


