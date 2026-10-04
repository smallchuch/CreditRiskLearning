SELECT * FROM (SELECT b.aggregator, b.broker_id, ROUND(SUM(l.original_amount),0) AS t, DENSE_RANK() OVER (PARTITION BY b.aggregator ORDER BY SUM(l.original_amount) DESC) AS r
FROM loan l JOIN dim_broker b USING (broker_id) GROUP BY 1,2) WHERE r<=2 ORDER BY 1, 4, 2
