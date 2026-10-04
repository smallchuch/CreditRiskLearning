SELECT COUNT(*), ROUND(SUM(original_amount),0) FROM loan WHERE origination_date > DATE '2025-12-31' - 365 AND origination_date <= DATE '2025-12-31'
