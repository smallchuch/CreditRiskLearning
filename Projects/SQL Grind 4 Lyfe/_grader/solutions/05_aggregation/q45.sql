SELECT year(origination_date), ROUND(AVG(original_amount),0), ROUND(AVG(lvr_at_origination_pct),1) FROM loan GROUP BY 1 ORDER BY 1
