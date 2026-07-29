-- foreign_keys.sql — RELATIONSHIP REFERENCE
-- ⚠ DuckDB does NOT support ALTER TABLE ADD FOREIGN KEY (tested: "not implemented").
-- These will NOT execute. Use this file two ways:
--   1) As documentation of the relationships.
--   2) As the spec for creating VIRTUAL (logical) foreign keys in DBeaver
--      (table editor → Foreign Keys tab → create logical FK → Ctrl+S).
-- To make them REAL enforced FKs you'd redefine each table with the FK inline in
-- CREATE TABLE and load via INSERT...SELECT, pointing SK_ID_CURR at a combined
-- train+test table to avoid enforced-FK orphan errors.

-- child.column                              -> parent.column
ALTER TABLE bureau                ADD FOREIGN KEY (SK_ID_CURR)   REFERENCES application_train (SK_ID_CURR);
ALTER TABLE bureau_balance        ADD FOREIGN KEY (SK_ID_BUREAU) REFERENCES bureau (SK_ID_BUREAU);
ALTER TABLE previous_application  ADD FOREIGN KEY (SK_ID_CURR)   REFERENCES application_train (SK_ID_CURR);
ALTER TABLE pos_cash_balance      ADD FOREIGN KEY (SK_ID_PREV)   REFERENCES previous_application (SK_ID_PREV);
ALTER TABLE pos_cash_balance      ADD FOREIGN KEY (SK_ID_CURR)   REFERENCES application_train (SK_ID_CURR);
ALTER TABLE credit_card_balance   ADD FOREIGN KEY (SK_ID_PREV)   REFERENCES previous_application (SK_ID_PREV);
ALTER TABLE credit_card_balance   ADD FOREIGN KEY (SK_ID_CURR)   REFERENCES application_train (SK_ID_CURR);
ALTER TABLE installments_payments ADD FOREIGN KEY (SK_ID_PREV)   REFERENCES previous_application (SK_ID_PREV);
ALTER TABLE installments_payments ADD FOREIGN KEY (SK_ID_CURR)   REFERENCES application_train (SK_ID_CURR);


