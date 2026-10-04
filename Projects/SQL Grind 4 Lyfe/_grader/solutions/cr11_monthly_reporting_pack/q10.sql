WITH m AS (SELECT CAST(date_trunc('month', origination_date) AS DATE) AS ms, SUM(original_amount) AS a FROM loan GROUP BY 1),
r AS (SELECT ms, SUM(a) OVER (ORDER BY ms ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) AS s, ROW_NUMBER() OVER (ORDER BY ms) AS rn FROM m)
SELECT ms, ROUND(s/1e6,1) FROM r WHERE month(ms)=12 AND rn>=12 ORDER BY ms
