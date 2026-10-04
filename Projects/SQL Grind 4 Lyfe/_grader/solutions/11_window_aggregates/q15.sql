WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, COUNT(*) AS n FROM loan GROUP BY 1)
SELECT * FROM (SELECT ms, n, LAG(n,12) OVER (ORDER BY ms) AS ly, ROUND(100.0*(n/LAG(n,12) OVER (ORDER BY ms)-1),1) FROM m) WHERE ms >= DATE '2025-01-01' ORDER BY ms
