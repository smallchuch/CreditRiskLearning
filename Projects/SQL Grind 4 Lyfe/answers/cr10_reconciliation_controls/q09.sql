-- ============================================================================
-- cr10_reconciliation_controls  |  Q09  |  ★★★ challenge
-- 
-- FULL OUTER JOIN reconciliation: loan counts by purpose in `loan` vs count of applications
-- that settled (`current_status='Settled'`) by purpose in `loan_application`. Show
-- `purpose`, `loans`, `settled_apps`, `diff`; sorted by purpose. (Internal refinance loans
-- have no application.)
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


