SELECT product_id, ROUND(AVG(interest_rate_at_origination_pct),3), ROUND(PERCENT_RANK() OVER (ORDER BY AVG(interest_rate_at_origination_pct)),2) FROM loan GROUP BY 1 ORDER BY 1
