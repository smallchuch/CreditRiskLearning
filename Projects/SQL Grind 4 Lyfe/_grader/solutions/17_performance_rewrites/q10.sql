SELECT COUNT(DISTINCT l.primary_customer_id) FROM loan l WHERE EXISTS (SELECT 1 FROM loan_monthly_snapshot s WHERE s.loan_id=l.loan_id AND s.days_past_due>=90)
