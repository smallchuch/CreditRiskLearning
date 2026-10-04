SELECT CASE current_status WHEN 'Settled' THEN 'Won' WHEN 'Declined' THEN 'Declined' ELSE 'Other' END AS outcome_group, COUNT(*) n FROM loan_application GROUP BY 1 ORDER BY 1
