SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE purpose='Purchase - Owner Occupied' INTERSECT SELECT primary_customer_id FROM loan WHERE purpose='Purchase - Investment')
