SELECT ROUND(100.0*COUNT(*) FILTER (WHERE verified_annual_amount IS NULL)/COUNT(*),2) FROM applicant_income
