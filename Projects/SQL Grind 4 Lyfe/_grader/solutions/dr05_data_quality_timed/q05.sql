SELECT COUNT(*) FROM loan_monthly_snapshot WHERE loan_status<>'Closed' AND (interest_rate_pct<1 OR interest_rate_pct>15)
