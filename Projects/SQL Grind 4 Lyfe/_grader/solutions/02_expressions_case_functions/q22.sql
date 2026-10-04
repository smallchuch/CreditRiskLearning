SELECT COUNT(*) FILTER (WHERE decision <> 'Approved'), COUNT(*) FILTER (WHERE decision IS DISTINCT FROM 'Approved') FROM loan_application
