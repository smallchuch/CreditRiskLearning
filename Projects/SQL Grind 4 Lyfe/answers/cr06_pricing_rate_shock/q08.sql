-- ============================================================================
-- cr06_pricing_rate_shock  |  Q08  |  ★★★ challenge
-- 
-- Stress test: for live P&I loans at 2025-12-31 compute each loan's current repayment from
-- balance, current rate and remaining term (`term_months - months_on_book`, floor 1), and
-- the repayment at +3pp. Report the total monthly repayment now and stressed (0dp) and %
-- increase (1dp) for loans with remaining term >= 12. `now_total`, `stress_total`,
-- `increase_pct`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


