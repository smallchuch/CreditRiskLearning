-- ============================================================================
-- 02_expressions_case_functions  |  Q07  |  ★★ core
-- 
-- Count loans by LVR band using CASE on `lvr_at_origination_pct`: `'<=60'`, `'60-80'` (above
-- 60 up to and including 80), `'>80'`. Return `lvr_band`, `loans`. Sorted by `loans`
-- descending.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 3 row(s). Sort the output as described.
-- ============================================================================

SELECT
        CASE 
                WHEN lvr_at_origination_pct <= 60 THEN '<=60'
                WHEN lvr_at_origination_pct BETWEEN 60 AND 80 THEN '60-80'
                WHEN lvr_at_origination_pct >= 80 THEN '>80'
                ELSE 'No LVR'
        END AS lvr_band,
        COUNT(*) AS loans
FROM loan
GROUP BY lvr_band
ORDER BY lvr_band ASC;

