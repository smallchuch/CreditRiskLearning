SELECT reporting_date, ROUND(SUM(ecl_amount),0) FROM ecl_provision_quarterly WHERE reporting_date>=DATE '2024-01-01' GROUP BY 1 ORDER BY 1
