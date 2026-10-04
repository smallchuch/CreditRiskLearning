SELECT COUNT(*) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.months_on_book=0 WHERE ABS(s.closing_balance-l.original_amount)>1
