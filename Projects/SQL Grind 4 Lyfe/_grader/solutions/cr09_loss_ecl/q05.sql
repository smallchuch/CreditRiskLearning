SELECT ifrs9_stage, ROUND(SUM(pd_12m*ead)/SUM(ead),4), ROUND(SUM(lgd*ead)/SUM(ead),4) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' GROUP BY 1 ORDER BY 1
