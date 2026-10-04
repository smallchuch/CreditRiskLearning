-- ============================================================================
-- 09_ctes  |  Q14  |  ★★★ challenge
-- 
-- Three-step arrears story: CTE `latest` = non-closed loans at 2025-12-31 with
-- `days_past_due`; CTE `bucketed` = bucket via CASE (`'Current'` 0, `'1-29'`, `'30-89'`,
-- `'90+'`); final = balance and loan count per bucket. Return `bucket`, `loans`, `balance`
-- (0dp); sorted by the bucket's severity (Current first).
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


