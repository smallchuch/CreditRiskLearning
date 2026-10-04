SELECT COUNT(*) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND days_past_due>=30 AND arrears_amount < scheduled_repayment
