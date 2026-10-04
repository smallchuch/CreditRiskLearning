SELECT COUNT(*), ROUND(SUM(original_amount),0) FROM loan WHERE origination_date>=DATE '2025-01-01' AND origination_date<DATE '2026-01-01'
