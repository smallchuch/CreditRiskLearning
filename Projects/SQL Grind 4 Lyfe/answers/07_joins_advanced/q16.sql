-- ============================================================================
-- 07_joins_advanced  |  Q16  |  ★★★ challenge
-- 
-- HPI revaluation join: index the loan's property to 2025-12-31. For loans 1-10 (non-
-- internal) get the property's state through `dim_postcode`, then the `price_index` for that
-- state at `month_end_date` = `last_day(origination_date)` and at `2025-12-31`. Return
-- `loan_id`, `idx_orig`, `idx_now`, `growth_pct` (1dp) = (now/orig-1)*100. Sorted by
-- `loan_id`.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 10 row(s). Sort the output as described.
-- ============================================================================


