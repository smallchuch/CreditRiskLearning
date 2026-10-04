SELECT primary_customer_id, COUNT(*) AS n FROM loan GROUP BY 1 HAVING COUNT(*) >= 4 ORDER BY n DESC, 1
