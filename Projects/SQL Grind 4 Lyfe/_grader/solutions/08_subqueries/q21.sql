SELECT COUNT(*) FROM loan WHERE purpose='Purchase - Investment' AND original_amount > (SELECT AVG(original_amount) FROM loan WHERE purpose='Purchase - Investment')
