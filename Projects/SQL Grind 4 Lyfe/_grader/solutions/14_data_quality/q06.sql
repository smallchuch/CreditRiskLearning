SELECT state, COUNT(*) AS n FROM customer WHERE state NOT IN ('NSW','VIC','QLD','SA','WA','TAS','NT','ACT') GROUP BY 1 ORDER BY n DESC, 1
