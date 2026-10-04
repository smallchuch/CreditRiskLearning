SELECT current_status, COUNT(*) AS n FROM loan_application WHERE decision IS NULL GROUP BY current_status ORDER BY current_status
