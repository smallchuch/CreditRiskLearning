SELECT COUNT(*) FROM (SELECT primary_customer_id, COUNT(*) AS n FROM loan GROUP BY 1) WHERE n=2
