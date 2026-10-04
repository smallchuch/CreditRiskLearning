-- ============================================================================
-- cr11_monthly_reporting_pack  |  Q07  |  ★★★ challenge
-- 
-- Balance roll-forward by month for 2025 (Feb-Dec): `opening` (prior month-end live
-- balance), `new_lending` (loans originated in the month), `closing` (live balance), and
-- `other_movements` = closing - opening - new_lending (repayments, closures, interest; 0dp).
-- `month_end`, `opening`, `new_lending`, `closing`, `other_movements`; sorted by date.
-- 
-- Return 5 column(s), in the order the question gives them.
-- Expected 11 row(s). Sort the output as described.
-- ============================================================================


