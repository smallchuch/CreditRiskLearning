SELECT CAST(date_trunc('month', closed_date) AS DATE), COUNT(*) FROM loan WHERE closed_date>=DATE '2025-01-01' AND closed_date<DATE '2026-01-01' GROUP BY 1 ORDER BY 1
