SELECT COUNT(*) FROM ecl_provision_quarterly WHERE lgd IS NOT NULL AND (lgd < 0 OR lgd > 1)
