SELECT customer_id, last_name || ', ' || first_name FROM customer WHERE customer_id <= 40 AND email IS NOT NULL AND mobile IS NOT NULL ORDER BY customer_id LIMIT 15
