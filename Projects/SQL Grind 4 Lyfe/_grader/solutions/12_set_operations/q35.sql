SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='Broker' EXCEPT SELECT primary_customer_id FROM loan WHERE channel<>'Broker')
