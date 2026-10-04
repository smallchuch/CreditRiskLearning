SELECT COUNT(*) FROM loan WHERE interest_rate_at_origination_pct IS NOT NULL AND (interest_rate_at_origination_pct < 1 OR interest_rate_at_origination_pct > 15)
