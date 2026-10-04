SELECT COUNT(*) FROM loan l JOIN dim_date d ON d.full_date = l.origination_date WHERE NOT d.is_business_day
