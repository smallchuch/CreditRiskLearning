SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan_application GROUP BY 1 HAVING COUNT(*)>=3 AND COUNT(*) FILTER (WHERE decision='Approved')=0)
