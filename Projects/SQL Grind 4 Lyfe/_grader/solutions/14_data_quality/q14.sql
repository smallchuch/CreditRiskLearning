SELECT COUNT(*) FROM (SELECT loan_id FROM loan_monthly_snapshot GROUP BY 1 HAVING COUNT(*) <> MAX(months_on_book)+1)
