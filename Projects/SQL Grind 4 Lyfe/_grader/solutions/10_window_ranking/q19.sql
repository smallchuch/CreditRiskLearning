WITH c AS (SELECT assessor_staff_id, COUNT(*) AS n FROM loan GROUP BY 1), t AS (SELECT n, NTILE(10) OVER (ORDER BY n, assessor_staff_id) AS d FROM c)
SELECT d, COUNT(*), ROUND(AVG(n),1) FROM t GROUP BY 1 ORDER BY 1
