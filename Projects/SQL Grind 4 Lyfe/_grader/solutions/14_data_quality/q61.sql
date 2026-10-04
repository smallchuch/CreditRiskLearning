SELECT COUNT(*) FROM loan WHERE original_amount IS NOT NULL AND (original_amount < 0 OR original_amount > 5000000)
