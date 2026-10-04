SELECT COUNT(*) FROM property_valuation c WHERE c.property_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM property p WHERE p.property_id=c.property_id)
