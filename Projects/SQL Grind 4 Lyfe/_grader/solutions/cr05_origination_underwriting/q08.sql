SELECT year(a.application_date), ROUND(100.0*COUNT(*) FILTER (WHERE s.hem_applied_flag)/COUNT(*),1) FROM loan_application a JOIN application_assessment s USING (application_id) GROUP BY 1 ORDER BY 1
