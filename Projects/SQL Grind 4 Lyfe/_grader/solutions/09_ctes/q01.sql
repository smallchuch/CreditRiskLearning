WITH big AS (SELECT * FROM loan WHERE original_amount > 1000000) SELECT purpose, COUNT(*) AS n FROM big GROUP BY 1 ORDER BY n DESC, 1
