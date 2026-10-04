SELECT customer_id, first_name || ' ' || last_name AS full_name FROM customer WHERE customer_id <= 8 ORDER BY customer_id
