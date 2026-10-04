WITH m AS (SELECT CAST(date_trunc('month', application_date) AS DATE) AS ms, COUNT(*) AS n FROM loan_application WHERE application_date >= DATE '2025-01-01' GROUP BY 1)
SELECT ms, n, SUM(n) OVER (ORDER BY ms) FROM m ORDER BY ms
