SELECT COUNT(*) FROM loan_monthly_snapshot WHERE days_past_due IS NOT NULL AND (days_past_due < 0 OR days_past_due > 2000)
