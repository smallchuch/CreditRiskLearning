SELECT COUNT(*) FROM ecl_provision_quarterly WHERE pd_12m IS NOT NULL AND (pd_12m < 0 OR pd_12m > 1)
