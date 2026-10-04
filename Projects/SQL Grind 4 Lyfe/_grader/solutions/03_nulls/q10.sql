SELECT income_type, COUNT(*) AS unverified FROM applicant_income WHERE verified_annual_amount IS NULL GROUP BY 1 ORDER BY 2 DESC, 1
