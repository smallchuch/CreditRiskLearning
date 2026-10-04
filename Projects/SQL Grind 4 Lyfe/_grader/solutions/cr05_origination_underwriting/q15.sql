SELECT COUNT(*) FROM loan_application a JOIN dim_broker b ON b.broker_id=a.broker_id WHERE a.application_date < b.accreditation_date
