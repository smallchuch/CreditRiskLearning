-- ============================================================================
-- 01_select_filter_sort  |  Q40  |  ★ warm-up
-- 
-- Postcodes in `'VIC'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by
-- `postcode`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 15 row(s). Sort the output as described.
-- ============================================================================


SELECT postcode, suburb, market_segment FROM dim_postcode
WHERE state = 'VIC'
ORDER BY postcode ASC;