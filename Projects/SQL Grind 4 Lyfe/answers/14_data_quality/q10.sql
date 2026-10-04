-- ============================================================================
-- 14_data_quality  |  Q10  |  ★★ core
-- 
-- Status vs date consistency: loans with `loan_status = 'Closed'` but NULL `closed_date`,
-- and loans with `loan_status <> 'Closed'` but a non-NULL `closed_date`. Two numbers.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


