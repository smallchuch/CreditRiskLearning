SELECT COUNT(*) FROM loan_application c WHERE c.assessor_staff_id IS NOT NULL AND NOT EXISTS (SELECT 1 FROM dim_staff p WHERE p.staff_id=c.assessor_staff_id)
