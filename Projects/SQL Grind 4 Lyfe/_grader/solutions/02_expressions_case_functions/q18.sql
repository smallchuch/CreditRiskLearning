SELECT application_id, GREATEST(monthly_surplus, 0), LEAST(nsr, 2) FROM application_assessment WHERE application_id <= 10 ORDER BY application_id
