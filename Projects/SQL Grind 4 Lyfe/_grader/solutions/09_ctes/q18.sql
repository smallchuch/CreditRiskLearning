WITH py AS (SELECT purpose, year(origination_date) AS yr, COUNT(*) AS n FROM loan GROUP BY 1,2),
mx AS (SELECT purpose, MAX(n) AS m FROM py GROUP BY 1)
SELECT py.purpose, py.yr, py.n FROM py JOIN mx ON mx.purpose=py.purpose AND mx.m=py.n ORDER BY 1,2
