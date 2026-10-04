SELECT COUNT(*), ROUND(SUM(ead),0) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND current_lvr_pct/0.9>100
