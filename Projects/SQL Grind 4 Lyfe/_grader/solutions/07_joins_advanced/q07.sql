SELECT (SELECT ROUND(SUM(original_amount),0) FROM loan), ROUND(SUM(l.original_amount),0) FROM loan l JOIN loan_borrower b USING (loan_id)
