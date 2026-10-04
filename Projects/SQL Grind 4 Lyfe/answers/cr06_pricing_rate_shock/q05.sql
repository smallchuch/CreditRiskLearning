-- ============================================================================
-- cr06_pricing_rate_shock  |  Q05  |  ★★ core
-- 
-- Retention discounts: loans that received a 'Retention discount' rate change - count, and
-- average discount in percentage points (the rate change at that effective date versus the
-- prior row's rate; 2dp). Use LAG on `loan_rate_history` per loan. `loans_discounted`,
-- `avg_cut_pp`. One row (cut positive).
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


