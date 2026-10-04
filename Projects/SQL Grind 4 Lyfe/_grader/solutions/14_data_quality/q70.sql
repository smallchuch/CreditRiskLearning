SELECT COUNT(*) FROM property WHERE year_built IS NOT NULL AND (year_built < 1850 OR year_built > 2026)
