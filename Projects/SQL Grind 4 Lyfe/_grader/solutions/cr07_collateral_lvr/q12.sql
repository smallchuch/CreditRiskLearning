SELECT ifrs9_stage, COUNT(*), ROUND(SUM(ead),0) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND current_lvr_pct>100 GROUP BY 1 ORDER BY 1
