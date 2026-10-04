SELECT stage_reason, COUNT(*) AS n FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND ifrs9_stage=2 GROUP BY 1 ORDER BY n DESC, 1
