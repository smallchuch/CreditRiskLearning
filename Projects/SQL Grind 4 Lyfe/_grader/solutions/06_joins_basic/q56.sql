SELECT l.purpose, COUNT(*) FROM hardship_arrangement h JOIN loan l USING (loan_id) WHERE h.hardship_type='Interest-only period' GROUP BY 1 ORDER BY 1
