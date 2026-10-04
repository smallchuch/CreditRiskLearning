SELECT decline_reason_code, COUNT(*) FROM loan_application WHERE decision='Declined' AND decline_reason_code IS NOT NULL GROUP BY 1 ORDER BY 2 DESC, 1
