-- ============================================================================
-- cr09_loss_ecl  |  Q10  |  ★★★ challenge
-- 
-- Back-test: for loans that defaulted (in `loan_loss`), what was their stage 4 quarters
-- before `default_date`? Use the latest reporting_date <= default_date - 1 year. Count by
-- stage. `ifrs9_stage`, `loans`; sorted by stage. (Were we early enough?)
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 2 row(s). Sort the output as described.
-- ============================================================================


