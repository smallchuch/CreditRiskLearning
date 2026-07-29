-- primary_keys.sql — real, enforced primary keys
-- DuckDB supports ALTER TABLE ADD PRIMARY KEY. Run these, then F5 the connection.

ALTER TABLE application_train    ADD PRIMARY KEY (SK_ID_CURR);
ALTER TABLE application_test     ADD PRIMARY KEY (SK_ID_CURR);
ALTER TABLE bureau               ADD PRIMARY KEY (SK_ID_BUREAU);
ALTER TABLE previous_application ADD PRIMARY KEY (SK_ID_PREV);
ALTER TABLE bureau_balance       ADD PRIMARY KEY (SK_ID_BUREAU, MONTHS_BALANCE);
ALTER TABLE pos_cash_balance     ADD PRIMARY KEY (SK_ID_PREV, MONTHS_BALANCE);
ALTER TABLE credit_card_balance  ADD PRIMARY KEY (SK_ID_PREV, MONTHS_BALANCE);

-- installments_payments: no reliably-unique key, so no primary key.