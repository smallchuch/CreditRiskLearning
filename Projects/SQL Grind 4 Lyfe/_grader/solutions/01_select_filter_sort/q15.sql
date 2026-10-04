SELECT application_id, requested_amount, policy_exception_reason FROM loan_application WHERE policy_exception_flag AND requested_amount >= 800000 ORDER BY requested_amount DESC, application_id
