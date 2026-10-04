SELECT d.fiscal_quarter, COUNT(*) FROM loan l JOIN dim_date d ON d.full_date=l.origination_date WHERE d.fiscal_year=2025 GROUP BY 1 ORDER BY 1
