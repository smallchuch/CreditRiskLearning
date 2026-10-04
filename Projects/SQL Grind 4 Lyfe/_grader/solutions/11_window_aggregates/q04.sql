WITH m AS (SELECT CAST(date_trunc('month', application_date) AS DATE) AS ms, COUNT(*) AS n FROM loan_application WHERE application_date >= DATE '2024-01-01' GROUP BY 1)
SELECT ms, n, ROUND(100.0*(n/LAG(n) OVER (ORDER BY ms)-1),1) FROM m ORDER BY ms
