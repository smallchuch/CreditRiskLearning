SELECT COUNT(*) FROM (SELECT 1 FROM customer WHERE date_of_birth IS NOT NULL GROUP BY LOWER(TRIM(first_name)), LOWER(TRIM(last_name)), date_of_birth HAVING COUNT(*)>1)
