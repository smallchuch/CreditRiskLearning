SELECT ROUND(100.0*COUNT(*) FILTER (WHERE fixed_rate_expiry_date IS NULL)/COUNT(*),2) FROM loan
