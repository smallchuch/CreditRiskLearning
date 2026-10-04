SELECT COUNT(*) FROM loan_application a JOIN dim_date d ON d.full_date = a.decision_date WHERE d.is_weekend
