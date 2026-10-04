SELECT year(origination_date), ROUND(AVG(interest_rate_at_origination_pct),3), ROUND(AVG(term_months),1) FROM loan GROUP BY 1 ORDER BY 1
