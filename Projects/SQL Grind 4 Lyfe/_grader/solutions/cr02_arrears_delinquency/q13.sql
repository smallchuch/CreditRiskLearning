WITH now AS (SELECT loan_id FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due>=30)
SELECT n, COUNT(*) FROM (SELECT s.loan_id, COUNT(*) FILTER (WHERE s.days_past_due>=30) AS n FROM loan_monthly_snapshot s JOIN now USING (loan_id) WHERE s.snapshot_date > DATE '2024-12-31' GROUP BY 1) GROUP BY 1 ORDER BY 1
