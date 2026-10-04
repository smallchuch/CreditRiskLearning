SELECT activity_type, COUNT(*), ROUND(100.0*COUNT(*) FILTER (WHERE promise_kept_flag)/COUNT(*),1) FROM collections_activity WHERE promise_amount IS NOT NULL GROUP BY 1 ORDER BY 1
