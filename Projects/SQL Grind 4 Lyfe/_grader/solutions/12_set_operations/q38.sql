SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan WHERE channel='Mobile Lender' EXCEPT SELECT primary_customer_id FROM loan WHERE channel<>'Mobile Lender')
