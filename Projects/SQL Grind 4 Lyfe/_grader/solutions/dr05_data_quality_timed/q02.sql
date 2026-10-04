SELECT COUNT(*) FROM customer WHERE date_of_birth IS NOT NULL AND (date_diff('year', date_of_birth, DATE '2025-12-31')<18 OR date_diff('year', date_of_birth, DATE '2025-12-31')>100)
