SELECT year(origination_date), COUNT(*) FILTER (WHERE rate_type='Fixed'), COUNT(*) FILTER (WHERE rate_type='Variable') FROM loan GROUP BY 1 ORDER BY 1
