-- ============================================================================
-- cr11_monthly_reporting_pack  |  Q06  |  ★★ core
-- 
-- Year-to-date new lending: monthly new amount and YTD cumulative (0dp) for 2024 and 2025
-- using `SUM() OVER (PARTITION BY year ORDER BY month)`. `yr`, `mon`, `new_amount`,
-- `ytd_amount`; sorted by year, month.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 24 row(s). Sort the output as described.
-- ============================================================================


