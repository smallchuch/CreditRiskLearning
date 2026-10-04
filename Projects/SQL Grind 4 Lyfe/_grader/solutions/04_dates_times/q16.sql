SELECT d.fiscal_year, COUNT(*) FROM loan l JOIN dim_date d ON d.full_date = l.origination_date GROUP BY 1 ORDER BY 1
