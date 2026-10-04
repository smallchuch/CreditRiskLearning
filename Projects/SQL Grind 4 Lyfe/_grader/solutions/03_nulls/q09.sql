SELECT ROUND(AVG(bureau_score),1), ROUND(AVG(COALESCE(bureau_score,0)),1) FROM credit_bureau_report
