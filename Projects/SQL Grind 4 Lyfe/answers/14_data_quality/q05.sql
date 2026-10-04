-- ============================================================================
-- 14_data_quality  |  Q05  |  ★★ core
-- 
-- Duplicate customers by normalised name + DOB: groups of rows with the same
-- `LOWER(TRIM(first_name))`, `LOWER(TRIM(last_name))` and `date_of_birth` (non-null). Return
-- the number of duplicate GROUPS. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


