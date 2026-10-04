-- ============================================================================
-- 07_joins_advanced  |  Q10  |  ★★ core
-- 
-- Which RBA cash rate applied to the bank on 2024-03-15? Range-join date to
-- `ref_rba_cash_rate` using `bank_effective_date` to the next row's effective date.
-- Simplest: return the `cash_rate_pct` of the latest row with `bank_effective_date <= DATE
-- '2024-03-15'`. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Sort the output as described.
-- ============================================================================


