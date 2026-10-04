SELECT COUNT(*) FILTER (WHERE is_business_day), COUNT(*) FILTER (WHERE is_public_holiday) FROM dim_date WHERE year=2022
