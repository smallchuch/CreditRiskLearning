SELECT COUNT(*) FROM customer c WHERE c.date_of_birth IS NULL AND EXISTS (
  SELECT 1 FROM customer d WHERE d.customer_id <> c.customer_id
    AND LOWER(TRIM(d.first_name)) = LOWER(TRIM(c.first_name)) AND LOWER(TRIM(d.last_name)) = LOWER(TRIM(c.last_name)) AND d.postcode = c.postcode)
