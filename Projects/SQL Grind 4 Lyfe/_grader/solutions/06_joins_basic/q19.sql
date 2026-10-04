SELECT a.channel, ROUND(AVG(i.inc),0) FROM loan_application a JOIN (SELECT application_id, SUM(COALESCE(verified_annual_amount, declared_annual_amount)) AS inc FROM applicant_income GROUP BY 1) i USING (application_id)
WHERE a.application_date >= DATE '2025-01-01' AND a.application_date < DATE '2026-01-01' GROUP BY 1 ORDER BY 1
