SELECT COUNT(*) FROM property c WHERE c.postcode IS NOT NULL AND NOT EXISTS (SELECT 1 FROM dim_postcode p WHERE p.postcode=c.postcode)
