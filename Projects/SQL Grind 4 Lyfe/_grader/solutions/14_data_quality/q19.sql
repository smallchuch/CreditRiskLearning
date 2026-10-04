SELECT COUNT(*) FROM loan_monthly_snapshot WHERE days_past_due>0 AND arrears_amount=0 AND NOT hardship_flag
