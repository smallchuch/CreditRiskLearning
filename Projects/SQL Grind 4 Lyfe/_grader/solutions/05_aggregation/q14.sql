SELECT purpose, ROUND(AVG(lvr_at_origination_pct),1) FROM loan WHERE purpose <> 'Internal Refinance' GROUP BY 1 ORDER BY 1
