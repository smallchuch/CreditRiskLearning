SELECT loan_id, ROUND(lvr_at_origination_pct/100,4) FROM loan WHERE loan_id <= 12 ORDER BY loan_id
