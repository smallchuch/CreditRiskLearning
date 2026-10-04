SELECT purpose, channel FROM loan INTERSECT SELECT purpose, channel FROM loan_application ORDER BY 1,2
