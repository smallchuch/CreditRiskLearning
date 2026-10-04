SELECT COUNT(*) FROM loan WHERE term_months IS NOT NULL AND (term_months < 12 OR term_months > 480)
