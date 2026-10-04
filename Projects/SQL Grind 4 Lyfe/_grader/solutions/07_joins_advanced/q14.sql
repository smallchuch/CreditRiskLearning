SELECT o.current_status, COUNT(*) AS n FROM loan_application r JOIN loan_application o ON o.application_id=r.resubmission_of_application_id GROUP BY 1 ORDER BY n DESC, 1
