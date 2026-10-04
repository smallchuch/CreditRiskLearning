SELECT CASE WHEN dti_ratio <= 4 THEN '<=4' WHEN dti_ratio <= 6 THEN '4-6' ELSE '>6' END AS dti_band, COUNT(*) FROM application_assessment GROUP BY 1 ORDER BY 1
