SELECT s, COUNT(*) FILTER (WHERE date_of_birth IS NULL) AS nd, COUNT(*) AS c, ROUND(100.0*COUNT(*) FILTER (WHERE date_of_birth IS NULL)/COUNT(*),2) AS pct
FROM (SELECT UPPER(TRIM(state)) AS s, date_of_birth FROM customer) WHERE LENGTH(s) <= 3 AND REPLACE(s,'.','')=s GROUP BY s HAVING 100.0*COUNT(*) FILTER (WHERE date_of_birth IS NULL)/COUNT(*) > 0.17 ORDER BY s
