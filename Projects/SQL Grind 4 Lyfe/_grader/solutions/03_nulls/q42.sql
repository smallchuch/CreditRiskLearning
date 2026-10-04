SELECT ROUND(100.0*COUNT(*) FILTER (WHERE manager_staff_id IS NULL)/COUNT(*),2) FROM dim_staff
