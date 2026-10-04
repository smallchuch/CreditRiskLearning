SELECT postcode, suburb, state FROM dim_postcode WHERE state IN ('NSW','VIC') AND market_segment='Regional' ORDER BY state, suburb
