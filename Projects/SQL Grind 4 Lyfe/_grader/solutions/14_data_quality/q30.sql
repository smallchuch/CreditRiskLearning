SELECT COUNT(*) FROM (SELECT report_id FROM credit_bureau_report GROUP BY 1 HAVING COUNT(*)>1)
