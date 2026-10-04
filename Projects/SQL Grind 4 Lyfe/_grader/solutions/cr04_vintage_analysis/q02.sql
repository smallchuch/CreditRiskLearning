SELECT year(origination_date), ROUND(AVG(lvr_at_origination_pct),1), ROUND(AVG(interest_rate_at_origination_pct),2) FROM loan GROUP BY 1 ORDER BY 1
