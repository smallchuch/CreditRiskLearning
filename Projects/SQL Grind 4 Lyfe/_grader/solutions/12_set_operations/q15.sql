SELECT stage, apps FROM (SELECT 'Lodged' AS stage, COUNT(*) AS apps FROM loan_application UNION ALL SELECT 'Decided', COUNT(*) FROM loan_application WHERE decision IS NOT NULL
UNION ALL SELECT 'Approved', COUNT(*) FROM loan_application WHERE decision='Approved' UNION ALL SELECT 'Settled', COUNT(*) FROM loan_application WHERE current_status='Settled') ORDER BY apps DESC
