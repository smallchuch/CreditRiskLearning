SELECT ROUND(100.0*COUNT(*) FILTER (WHERE end_date IS NULL)/COUNT(*),2) FROM hardship_arrangement
