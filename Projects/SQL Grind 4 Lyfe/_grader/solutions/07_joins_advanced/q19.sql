SELECT COUNT(*) FROM loan l JOIN dim_staff s ON s.staff_id=l.assessor_staff_id WHERE l.original_amount > s.lending_authority_limit
