SELECT customer_id, LEFT(first_name,1) || LEFT(last_name,1) FROM customer WHERE customer_id <= 40 AND email IS NOT NULL AND mobile IS NOT NULL ORDER BY customer_id LIMIT 15
