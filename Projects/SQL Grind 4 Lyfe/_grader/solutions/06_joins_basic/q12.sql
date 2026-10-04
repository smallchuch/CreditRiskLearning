SELECT r.reason_category, COUNT(*) AS n FROM loan_application a JOIN ref_decline_reason r ON r.reason_code=a.decline_reason_code GROUP BY 1 ORDER BY n DESC, 1
