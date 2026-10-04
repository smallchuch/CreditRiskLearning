SELECT COUNT(*), COUNT(*) FILTER (WHERE purpose='Internal Refinance') FROM loan WHERE application_id IS NULL
