SELECT ROUND(AVG(interest_rate_pct),3) FROM loan_rate_history WHERE effective_from<=DATE '2025-06-30' AND (effective_to IS NULL OR effective_to>DATE '2025-06-30') AND interest_rate_pct>=1
