-- ============================================================================
-- 16_ddl_dml_views  |  Q16  |  ★★★ challenge
-- 
-- Slowly changing dimension (type 2) by hand: create `scratch.cust_scd (customer_id,
-- segment, valid_from DATE, valid_to DATE, is_current BOOLEAN)` with
-- (1,'Mass','2020-01-01',NULL,true). Then close that row (`valid_to='2023-06-30'`,
-- `is_current=false`) and insert (1,'Premium','2023-07-01',NULL,true). SELECT all rows
-- sorted by `valid_from`.
-- 
-- Return 5 column(s), in the order the question gives them.
-- Expected 2 row(s). Sort the output as described.
-- ============================================================================


