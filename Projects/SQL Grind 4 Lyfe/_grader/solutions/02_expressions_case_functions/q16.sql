SELECT COUNT(*) FROM loan WHERE ABS(original_amount / security_value_at_origination * 100 - lvr_at_origination_pct) > 0.01
