SELECT COUNT(*) FROM (SELECT property_id, MAX(valuation_date) AS d FROM property_valuation GROUP BY 1) WHERE DATE '2025-12-31' - d > 730
