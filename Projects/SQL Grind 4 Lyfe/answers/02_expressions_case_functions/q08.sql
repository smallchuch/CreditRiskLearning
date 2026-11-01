-- ============================================================================
-- 02_expressions_case_functions  |  Q08  |  ★★ core
-- 
-- Debt-to-income bands from `application_assessment`: `'<=4'`, `'4-6'` (above 4 up to and
-- including 6), `'>6'`. Return `dti_band`, `applications`. Sorted by `dti_band`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 3 row(s). Sort the output as described.
-- ============================================================================


SELECT
        CASE
                WHEN dti_ratio <= 4 THEN '<=4'
                WHEN dti_ratio BETWEEN 4 AND 6 THEN '4-6'
                WHEN dti_ratio > 6 THEN '>6'
                ELSE 'No DTI'
        END AS dti_band,
        COUNT(*) as applications
FROM application_assessment
GROUP BY dti_band
ORDER BY dti_band ASC;