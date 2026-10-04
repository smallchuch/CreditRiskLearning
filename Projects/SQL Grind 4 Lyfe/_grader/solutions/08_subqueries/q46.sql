SELECT ROUND(AVG(n),2) FROM (SELECT primary_customer_id, COUNT(*) AS n FROM loan WHERE channel='Broker' GROUP BY 1)
