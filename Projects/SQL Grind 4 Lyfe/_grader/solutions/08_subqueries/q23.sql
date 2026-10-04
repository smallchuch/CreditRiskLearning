SELECT COUNT(*) FROM loan WHERE purpose='Equity Release / Top-up' AND original_amount > (SELECT AVG(original_amount) FROM loan WHERE purpose='Equity Release / Top-up')
