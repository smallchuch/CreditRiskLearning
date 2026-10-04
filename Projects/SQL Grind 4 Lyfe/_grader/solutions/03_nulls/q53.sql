SELECT ROUND(AVG(COALESCE(io_period_months,0)),2), ROUND(AVG(io_period_months),2) FROM loan WHERE purpose='Equity Release / Top-up'
