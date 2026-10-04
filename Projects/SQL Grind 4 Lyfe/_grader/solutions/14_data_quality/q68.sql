SELECT COUNT(*) FROM loan_application WHERE dependants IS NOT NULL AND (dependants < 0 OR dependants > 10)
