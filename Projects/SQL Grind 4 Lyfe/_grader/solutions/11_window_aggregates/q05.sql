WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan GROUP BY 1),
w AS (SELECT ms, n, ROUND(AVG(n) OVER (ORDER BY ms ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),1) AS ma FROM m)
SELECT ms, n, ma FROM w WHERE ms >= DATE '2025-01-01' ORDER BY ms
