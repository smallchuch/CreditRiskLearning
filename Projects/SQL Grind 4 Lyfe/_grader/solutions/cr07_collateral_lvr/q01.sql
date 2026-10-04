SELECT valuation_type, COUNT(*) AS n FROM property_valuation GROUP BY 1 ORDER BY n DESC, 1
