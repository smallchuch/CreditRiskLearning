SELECT valuation_type, COUNT(*) FROM property_valuation WHERE valuation_amount=0 GROUP BY 1 HAVING COUNT(*)>0 ORDER BY 1
