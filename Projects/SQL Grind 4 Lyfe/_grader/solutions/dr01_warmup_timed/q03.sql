SELECT ROUND(100.0*COUNT(*) FILTER (WHERE decision='Declined')/COUNT(*),1) FROM loan_application
