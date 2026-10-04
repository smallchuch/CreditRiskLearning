-- ============================================================================
-- cr11_monthly_reporting_pack  |  Q10  |  ★★★ challenge
-- 
-- Rolling 12-month new lending: for each month-end from Dec 2019 to Dec 2025, the sum of new
-- lending in the latest 12 months ($m, 1dp). Use a window `ROWS BETWEEN 11 PRECEDING AND
-- CURRENT ROW` over a monthly series. Return only the December rows: `month_start`,
-- `rolling_12m_m`; sorted by month.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 7 row(s). Sort the output as described.
-- ============================================================================


