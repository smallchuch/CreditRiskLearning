SELECT income_type, ROUND(100.0*COUNT(*) FILTER (WHERE verified_annual_amount IS NULL)/COUNT(*),1) AS p FROM applicant_income GROUP BY 1 ORDER BY p DESC, 1
