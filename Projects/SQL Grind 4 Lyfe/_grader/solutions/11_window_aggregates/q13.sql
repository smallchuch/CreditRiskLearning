SELECT loan_id, months_on_book, closing_balance, d FROM (SELECT loan_id, months_on_book, closing_balance, ROUND(closing_balance-FIRST_VALUE(closing_balance) OVER (PARTITION BY loan_id ORDER BY snapshot_date),2) AS d FROM loan_monthly_snapshot WHERE loan_id<=5)
WHERE months_on_book <= 4 ORDER BY 1,2
