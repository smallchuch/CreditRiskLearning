SELECT year(received_date), COUNT(*), ROUND(MEDIAN(resolved_date-received_date),1) FROM complaint WHERE category IN ('Hardship handling','Collections conduct') GROUP BY 1 ORDER BY 1
