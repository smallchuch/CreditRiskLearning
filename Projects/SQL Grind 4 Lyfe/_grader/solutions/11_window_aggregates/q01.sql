WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan WHERE origination_date >= DATE '2023-01-01' AND origination_date < DATE '2024-01-01' GROUP BY 1)
SELECT ms, ROUND(a,0), ROUND(LAG(a) OVER (ORDER BY ms),0) FROM m ORDER BY ms
