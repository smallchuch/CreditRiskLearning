SELECT COUNT(*) FROM loan WHERE purpose='Construction' AND original_amount > (SELECT AVG(original_amount) FROM loan WHERE purpose='Construction')
