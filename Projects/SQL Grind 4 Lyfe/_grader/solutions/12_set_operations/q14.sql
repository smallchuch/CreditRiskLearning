SELECT yr, mon, loans FROM (SELECT 2023 AS yr, month(origination_date) AS mon, COUNT(*) AS loans FROM loan WHERE year(origination_date)=2023 GROUP BY 2
UNION ALL SELECT 2024, month(origination_date), COUNT(*) FROM loan WHERE year(origination_date)=2024 GROUP BY 2
UNION ALL SELECT 2025, month(origination_date), COUNT(*) FROM loan WHERE year(origination_date)=2025 GROUP BY 2) WHERE mon <= 3 ORDER BY 1,2
