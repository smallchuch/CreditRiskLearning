SELECT CASE WHEN bureau_score IS NULL THEN 'Thin file' WHEN bankruptcy_flag OR court_judgements > 0 THEN 'Adverse'
  WHEN bureau_score < 600 THEN 'Weak' WHEN bureau_score < 750 THEN 'Fair' ELSE 'Strong' END AS quality, COUNT(*) AS reports
FROM credit_bureau_report GROUP BY 1 ORDER BY 2 DESC, 1
