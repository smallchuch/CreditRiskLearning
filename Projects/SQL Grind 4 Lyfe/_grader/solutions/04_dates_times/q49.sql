SELECT dayname(application_date), COUNT(*) FROM loan_application WHERE application_date >= DATE '2025-01-01' AND application_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1
