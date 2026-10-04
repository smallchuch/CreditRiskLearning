SELECT application_id, purpose, decline_reason_code FROM loan_application WHERE purpose IN ('Construction','Equity Release / Top-up') AND current_status='Declined' ORDER BY application_id
