SELECT b.broker_tier, ROUND(100.0*COUNT(*) FILTER (WHERE a.decision='Approved')/COUNT(a.decision),1) FROM loan_application a JOIN dim_broker b USING (broker_id) GROUP BY 1 ORDER BY 1
