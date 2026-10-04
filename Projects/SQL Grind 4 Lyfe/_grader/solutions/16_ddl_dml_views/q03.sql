CREATE OR REPLACE VIEW scratch.v_active AS SELECT loan_id, product_id, original_amount FROM loan WHERE loan_status='Active'; SELECT COUNT(*) FROM scratch.v_active
