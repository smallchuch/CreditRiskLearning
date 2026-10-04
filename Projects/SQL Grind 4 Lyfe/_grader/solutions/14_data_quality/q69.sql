SELECT COUNT(*) FROM property WHERE bedrooms IS NOT NULL AND (bedrooms < 1 OR bedrooms > 12)
