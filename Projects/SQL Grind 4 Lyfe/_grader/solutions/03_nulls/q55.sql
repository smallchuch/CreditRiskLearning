SELECT COALESCE(decision,'(none)') AS d, COUNT(*), COUNT(decline_reason_code) FROM loan_application GROUP BY 1 ORDER BY 1
