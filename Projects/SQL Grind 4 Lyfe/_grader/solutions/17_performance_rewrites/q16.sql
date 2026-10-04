SELECT payment_status, COUNT(*), ROUND(SUM(payment_amount),0) FROM loan_payment WHERE payment_date > DATE '2025-09-30' AND payment_date <= DATE '2025-12-31' GROUP BY 1 ORDER BY 1
