SELECT b.aggregator, ROUND(SUM(l.original_amount),0) AS t FROM loan l JOIN dim_broker b ON b.broker_id=l.broker_id GROUP BY 1 ORDER BY t DESC
