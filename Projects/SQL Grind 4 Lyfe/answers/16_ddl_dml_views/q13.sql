-- ============================================================================
-- 16_ddl_dml_views  |  Q13  |  ★★★ challenge
-- 
-- Views over views: `scratch.v1` = loans with `original_amount > 1000000`; `scratch.v2` = v1
-- joined to `dim_product` giving `product_name` and `loan_id`. SELECT `product_name`,
-- `loans` from v2 sorted by loans descending, then product_name, top 5 rows.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 5 row(s). Sort the output as described.
-- ============================================================================


