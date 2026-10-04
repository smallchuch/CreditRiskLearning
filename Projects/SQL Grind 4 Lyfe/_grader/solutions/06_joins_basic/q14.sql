SELECT l.purpose, COUNT(*) AS n FROM hardship_arrangement h JOIN loan l USING (loan_id) GROUP BY 1 ORDER BY n DESC, 1
