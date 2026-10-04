-- ============================================================================
-- 16_ddl_dml_views  |  Q15  |  ★★★ challenge
-- 
-- Constraint check: create `scratch.t5 (id INTEGER NOT NULL, amt DOUBLE CHECK (amt >= 0))`,
-- insert (1, 10.5), (2, 0), then SELECT `id`, `amt` sorted by id. (Think: what would happen
-- if you inserted a negative amount?)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 2 row(s). Sort the output as described.
-- ============================================================================


