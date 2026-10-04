SELECT loan_id, io_period_months, io_expiry_date FROM loan WHERE io_period_months > 0 AND io_expiry_date <= DATE '2025-12-31' AND loan_status='Active' ORDER BY io_expiry_date, loan_id
