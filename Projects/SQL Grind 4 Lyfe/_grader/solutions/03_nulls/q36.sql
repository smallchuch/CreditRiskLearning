SELECT ROUND(100.0*COUNT(*) FILTER (WHERE bureau_score IS NULL)/COUNT(*),2) FROM credit_bureau_report
