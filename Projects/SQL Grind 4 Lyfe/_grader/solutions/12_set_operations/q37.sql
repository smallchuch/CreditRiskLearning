SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='Digital' EXCEPT SELECT primary_customer_id FROM loan WHERE channel<>'Digital')
