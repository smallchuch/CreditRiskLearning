-- ============================================================================
-- 01_select_filter_sort  |  Q42  |  ★ warm-up
-- 
-- Postcodes in `'SA'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by
-- `postcode`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 35 row(s). Sort the output as described.
-- ============================================================================


SELECT postcode, suburb, market_segment FROM dim_postcode
WHERE state = 'SA'
ORDER BY postcode ASC;