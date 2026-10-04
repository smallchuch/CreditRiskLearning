SELECT ROUND(100.0*COUNT(*) FILTER (WHERE lmi_flag)/COUNT(*),2) FROM loan WHERE lvr_at_origination_pct>80
