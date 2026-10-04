SELECT ROUND(100.0*COUNT(*) FILTER (WHERE promise_amount IS NULL)/COUNT(*),2) FROM collections_activity
