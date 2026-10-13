-- ============================================================================
-- 01_select_filter_sort  |  Q23  |  ★★★ challenge
-- 
-- Properties: houses with at least 4 bedrooms and a land area over 1,000 sqm built after
-- 2010. Return `property_id`, `bedrooms`, `land_area_sqm`, `year_built`; sorted by
-- `land_area_sqm` desc, `property_id`. Use only the `property` table.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 781 row(s). Sort the output as described.
-- ============================================================================


SELECT property_id, bedrooms, land_area_sqm, year_built FROM property
WHERE bedrooms >= 4
AND year_built > 2010
AND land_area_sqm > 1000
AND property_type = 'House'
ORDER BY land_area_sqm DESC, property_id ASC;