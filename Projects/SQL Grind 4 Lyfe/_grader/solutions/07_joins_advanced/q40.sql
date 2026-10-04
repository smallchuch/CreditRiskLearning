SELECT ROUND((SELECT SUM(original_amount) FROM loan WHERE purpose='Construction'),0), ROUND(SUM(l.original_amount),0) FROM loan l JOIN loan_borrower b USING (loan_id) WHERE l.purpose='Construction'
