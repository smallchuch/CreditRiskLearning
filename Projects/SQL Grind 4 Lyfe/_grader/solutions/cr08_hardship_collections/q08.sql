SELECT failure_reason, COUNT(*) AS n FROM loan_payment WHERE payment_status='Dishonoured' GROUP BY 1 ORDER BY n DESC, 1
