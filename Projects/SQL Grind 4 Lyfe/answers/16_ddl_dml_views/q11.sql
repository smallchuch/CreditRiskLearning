-- ============================================================================
-- 16_ddl_dml_views  |  Q11  |  ★★★ challenge
-- 
-- Upsert: create `scratch.limits (staff_id INTEGER PRIMARY KEY, lim INTEGER)` filled from
-- `dim_staff` for staff 1-5 (`lending_authority_limit`). Then `INSERT ... ON CONFLICT
-- (staff_id) DO UPDATE SET lim = excluded.lim` for rows (3, 999999), (6, 123456). SELECT
-- `staff_id`, `lim` sorted by `staff_id` for ids 1-6.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


