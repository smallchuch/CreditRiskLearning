-- ============================================================================
-- 04_dates_times  |  Q17  |  ★★★ challenge
-- 
-- Settlement lag: for settled applications that became loans (join `loan_application` to
-- `loan` on `application_id`), the average days from `application_date` to
-- `origination_date`, rounded to 1 dp, by application `channel`. Return `channel`,
-- `avg_days`; sorted by `channel`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


