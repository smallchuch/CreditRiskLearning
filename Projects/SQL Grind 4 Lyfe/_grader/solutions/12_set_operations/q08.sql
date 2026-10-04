SELECT COUNT(*) FROM (SELECT application_id FROM credit_bureau_report EXCEPT SELECT application_id FROM application_assessment)
