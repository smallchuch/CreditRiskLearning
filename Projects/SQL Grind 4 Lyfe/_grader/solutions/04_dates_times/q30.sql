SELECT quarter(origination_date), COUNT(*) FROM loan WHERE origination_date >= DATE '2025-01-01' AND origination_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1
