SELECT COUNT(*) FROM credit_bureau_report WHERE bureau_score IS NOT NULL AND (bureau_score < 300 OR bureau_score > 1200)
