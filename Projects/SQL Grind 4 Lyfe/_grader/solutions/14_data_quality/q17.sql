SELECT * FROM (
SELECT 'collections_activity' AS tbl, COUNT(*) AS n FROM collections_activity WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'ecl_provision_quarterly', COUNT(*) FROM ecl_provision_quarterly WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'hardship_arrangement', COUNT(*) FROM hardship_arrangement WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_loss', COUNT(*) FROM loan_loss WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_monthly_snapshot', COUNT(*) FROM loan_monthly_snapshot WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_payment', COUNT(*) FROM loan_payment WHERE loan_id NOT IN (SELECT loan_id FROM loan)
UNION ALL SELECT 'loan_rate_history', COUNT(*) FROM loan_rate_history WHERE loan_id NOT IN (SELECT loan_id FROM loan)) ORDER BY 1
