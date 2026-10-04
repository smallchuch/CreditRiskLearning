SELECT COUNT(*) FROM loan_monthly_snapshot WHERE interest_rate_pct IS NOT NULL AND (interest_rate_pct < 1 OR interest_rate_pct > 15)
