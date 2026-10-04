WITH a AS (SELECT COUNT(*) AS n FROM loan), b AS (SELECT COUNT(*) AS n FROM loan_application) SELECT a.n, b.n, ROUND(100.0*a.n/b.n,1) FROM a, b
