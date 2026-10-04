SELECT COUNT(*) FROM loan WHERE ABS(maturity_date - CAST(origination_date + INTERVAL 1 MONTH * term_months AS DATE)) > 3
