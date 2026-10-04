SELECT loan_id, interest_rate_pct FROM loan_rate_history WHERE loan_id <= 20 AND effective_from <= DATE '2020-06-30' AND (effective_to IS NULL OR effective_to > DATE '2020-06-30') ORDER BY 1
