-- ============================================================================
-- 14_data_quality  |  Q15  |  ★★★ challenge
-- 
-- Find the actual missing snapshot months: for loans 1-5000, list `loan_id` and the
-- `months_on_book` values missing between 0 and the loan's max. Use a generate_series/unnest
-- spine. Return `loan_id`, `missing_mob`; sorted by both. (Few rows.)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 668 row(s). Sort the output as described.
-- ============================================================================


