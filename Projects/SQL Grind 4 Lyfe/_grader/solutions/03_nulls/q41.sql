SELECT ROUND(100.0*COUNT(*) FILTER (WHERE termination_date IS NULL)/COUNT(*),2) FROM dim_staff
