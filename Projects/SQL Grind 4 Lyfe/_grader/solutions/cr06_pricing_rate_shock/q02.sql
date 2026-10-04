SELECT year(origination_date), ROUND(AVG(interest_rate_at_origination_pct),3) FROM loan WHERE rate_type='Variable' GROUP BY 1 ORDER BY 1
