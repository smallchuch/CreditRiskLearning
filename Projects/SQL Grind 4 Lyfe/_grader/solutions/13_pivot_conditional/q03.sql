SELECT * FROM (PIVOT loan ON loan_status IN ('Active','Closed','In Recovery') USING COUNT(*) GROUP BY channel) ORDER BY channel
