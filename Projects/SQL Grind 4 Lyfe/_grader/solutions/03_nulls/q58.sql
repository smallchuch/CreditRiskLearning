SELECT (SELECT ROUND(AVG(bureau_score),2) FROM credit_bureau_report), (SELECT ROUND(AVG(a),2) FROM (SELECT AVG(bureau_score) AS a FROM credit_bureau_report GROUP BY enquiries_last_12m))
