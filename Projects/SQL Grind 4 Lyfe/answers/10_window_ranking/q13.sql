-- ============================================================================
-- 10_window_ranking  |  Q13  |  ★★★ challenge
-- 
-- De-duplicate customers: the `customer` table has duplicate people (same lower/trimmed name
-- + date_of_birth, ignoring NULL DOB). Number duplicates within each person with ROW_NUMBER
-- ordered by `customer_id`, then count how many extra (rn > 1) rows exist. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


