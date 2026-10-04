SELECT COUNT(*) FROM loan WHERE lvr_at_origination_pct IS NOT NULL AND (lvr_at_origination_pct < 1 OR lvr_at_origination_pct > 105)
