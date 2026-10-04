SELECT COUNT(*) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND ABS(ecl_amount - ead*lgd*CASE WHEN ifrs9_stage=1 THEN pd_12m ELSE pd_lifetime END) > 1
