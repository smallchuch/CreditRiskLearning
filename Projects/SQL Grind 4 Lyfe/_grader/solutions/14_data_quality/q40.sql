SELECT COUNT(*) FROM (SELECT valuation_id FROM property_valuation GROUP BY 1 HAVING COUNT(*)>1)
