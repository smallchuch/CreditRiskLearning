-- ============================================================================
-- 03_nulls  |  Q12  |  ★★ core
-- 
-- Safe division. For loan 1..30 compute `original_amount / NULLIF(io_period_months,0)`
-- rounded to 2 dp (monthly principal-like figure). Return `loan_id`, value; sorted by
-- `loan_id`. Loans with no IO period will show NULL rather than an error.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 30 row(s). Sort the output as described.
-- ============================================================================


