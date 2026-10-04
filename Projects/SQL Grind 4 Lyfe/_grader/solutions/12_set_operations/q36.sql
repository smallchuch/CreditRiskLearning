SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='Branch' EXCEPT SELECT primary_customer_id FROM loan WHERE channel<>'Branch')
