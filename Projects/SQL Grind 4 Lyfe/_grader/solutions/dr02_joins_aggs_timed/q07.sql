SELECT l.channel, ROUND(100.0*COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM loan_borrower b WHERE b.loan_id=l.loan_id AND b.borrower_role='Co-applicant'))/COUNT(*),1) FROM loan l GROUP BY 1 ORDER BY 1
