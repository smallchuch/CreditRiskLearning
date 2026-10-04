-- ============================================================================
-- 14_data_quality  |  Q14  |  ★★★ challenge
-- 
-- Missing monthly snapshots (gaps): for each loan the expected number of snapshot rows
-- equals `months on book + 1` through its last snapshot. Count loans where the number of
-- snapshot rows differs from `MAX(months_on_book) + 1`. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


