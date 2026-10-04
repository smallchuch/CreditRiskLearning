SELECT ROUND(SUM(COALESCE(verified_annual_amount, declared_annual_amount)),0) FROM applicant_income
