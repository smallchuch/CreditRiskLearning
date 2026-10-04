WITH s AS (SELECT current_status, COUNT(*) AS n FROM loan_application GROUP BY 1) SELECT current_status, ROUND(100.0*n/SUM(n) OVER (),1) AS p FROM s ORDER BY p DESC, 1
