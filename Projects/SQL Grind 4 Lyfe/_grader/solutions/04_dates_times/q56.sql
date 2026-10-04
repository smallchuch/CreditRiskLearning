SELECT ROUND(AVG((closed_date-origination_date)/365.25),2) FROM loan WHERE closed_date IS NOT NULL AND closed_date >= DATE '2025-01-01' AND closed_date < DATE '2026-01-01'
