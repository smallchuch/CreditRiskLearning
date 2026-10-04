SELECT rate_type, year(origination_date), ROUND(AVG(interest_rate_at_origination_pct),2) FROM loan GROUP BY 1,2 ORDER BY 1,2
