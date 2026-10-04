SELECT loan_id, lvr_at_origination_pct FROM loan WHERE lvr_at_origination_pct > 90 AND NOT lmi_flag ORDER BY loan_id
