-- ============================================================================
-- 14_data_quality  |  Q16  |  ★★★ challenge
-- 
-- Islands: for loan 1..N, consecutive-month arrears runs. Using gaps-and-islands on
-- `loan_monthly_snapshot` (non-closed rows with `days_past_due >= 30`), find the longest
-- consecutive run of 30+ DPD snapshot months for any loan. One number: `max_run`. Hint:
-- `months_on_book - ROW_NUMBER() OVER (PARTITION BY loan_id ORDER BY months_on_book)` is
-- constant within an island.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


