SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE purpose='Purchase - Investment' INTERSECT SELECT primary_customer_id FROM loan WHERE purpose='Equity Release / Top-up')
