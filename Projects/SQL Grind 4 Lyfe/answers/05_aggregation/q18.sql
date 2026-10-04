-- ============================================================================
-- 05_aggregation  |  Q18  |  ★★★ challenge
-- 
-- Arrears rate. At 2025-12-31, for non-closed loans: `loans`, `loans_30plus` (days_past_due
-- >= 30), `loans_90plus` (>= 90), and the 90+ rate as % of balance (2 dp) = SUM(balance
-- where dpd>=90)/SUM(balance)*100. Return the four values as one row: loans, loans_30plus,
-- loans_90plus, pct_balance_90plus.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


