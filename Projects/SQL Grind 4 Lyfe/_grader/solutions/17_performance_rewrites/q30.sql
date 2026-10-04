SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='Branch' GROUP BY 1 HAVING COUNT(*)>=3)
