CREATE TABLE application_train AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/application_train.csv');

CREATE TABLE bureau AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/bureau.csv');

CREATE TABLE previous_application AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/previous_application.csv');


CREATE TABLE application_test AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/application_test.csv');


CREATE TABLE bureau_balance AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/bureau_balance.csv');


CREATE TABLE credit_card_balance AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/credit_card_balance.csv');


CREATE TABLE HomeCredit_column_descriptions AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/HomeCredit_column_descriptions.csv');


CREATE TABLE intallments_payments AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/installment_payments.csv');


CREATE TABLE pos_cash_balance AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/POS_CASH_balance.csv');


CREATE TABLE previous_application AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/previous_application.csv');

CREATE TABLE installment_payments AS
SELECT * FROM read_csv_auto('C:/Dev/CreditRiskLearning/Datasets/Home Credit Default Risk/installments_payments.csv');
