-- ============================================================================
-- 01_select_filter_sort  |  Q39  |  ★ warm-up
-- 
-- Postcodes in `'NSW'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by
-- `postcode`.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 15 row(s). Sort the output as described.
-- ============================================================================


SELECT postcode, suburb, market_segment FROM dim_postcode
WHERE state = 'NSW'
ORDER BY postcode ASC;