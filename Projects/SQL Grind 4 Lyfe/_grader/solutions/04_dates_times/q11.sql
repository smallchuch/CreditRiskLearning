SELECT customer_id, date_diff('year', date_of_birth, DATE '2025-12-31') FROM customer WHERE customer_id <= 10 AND date_of_birth IS NOT NULL ORDER BY customer_id
