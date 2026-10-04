SELECT COUNT(*), ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM customer),2) FROM customer c WHERE NOT EXISTS (SELECT 1 FROM dim_postcode p WHERE p.postcode=c.postcode)
