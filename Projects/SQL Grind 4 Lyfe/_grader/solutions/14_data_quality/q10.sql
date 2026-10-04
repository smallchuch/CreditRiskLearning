SELECT COUNT(*) FILTER (WHERE loan_status='Closed' AND closed_date IS NULL), COUNT(*) FILTER (WHERE loan_status<>'Closed' AND closed_date IS NOT NULL) FROM loan
