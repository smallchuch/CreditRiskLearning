WITH apps AS (SELECT * FROM loan_application WHERE application_date >= DATE '2025-01-01' AND application_date < DATE '2026-01-01'),
settled AS (SELECT * FROM apps WHERE current_status='Settled')
SELECT (SELECT COUNT(*) FROM apps), (SELECT COUNT(*) FROM settled), ROUND(100.0*(SELECT COUNT(*) FROM settled)/(SELECT COUNT(*) FROM apps),1)
