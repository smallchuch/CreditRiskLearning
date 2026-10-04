SELECT year(a.application_date), COUNT(*) FROM loan_application a JOIN application_assessment s USING (application_id) WHERE a.decision='Approved' AND s.dti_ratio>=6 GROUP BY 1 ORDER BY 1
