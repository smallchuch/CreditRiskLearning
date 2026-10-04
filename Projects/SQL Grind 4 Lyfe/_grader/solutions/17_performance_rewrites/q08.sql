SELECT COUNT(*) FILTER (WHERE decision='Approved'), COUNT(*) FILTER (WHERE decision='Declined'), COUNT(*) FILTER (WHERE current_status='Withdrawn') FROM loan_application
