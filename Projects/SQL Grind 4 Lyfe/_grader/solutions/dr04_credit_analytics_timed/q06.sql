SELECT ROUND(100*SUM(ead) FILTER (WHERE ifrs9_stage>=2)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31'
