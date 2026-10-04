SELECT loan_id, origination_date FROM loan WHERE origination_date >= DATE '2025-01-01' AND day(origination_date) >= 28 AND (original_amount > 700000 OR lvr_at_origination_pct > 95) ORDER BY loan_id
