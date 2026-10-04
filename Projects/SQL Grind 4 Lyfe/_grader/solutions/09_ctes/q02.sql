WITH y AS (SELECT year(origination_date) AS yr, COUNT(*) AS n FROM loan GROUP BY 1) SELECT yr, n FROM y WHERE n > 9000 ORDER BY 1
