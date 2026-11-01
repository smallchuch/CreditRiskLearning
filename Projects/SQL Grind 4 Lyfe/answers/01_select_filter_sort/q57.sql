-- ============================================================================
-- 01_select_filter_sort  |  Q57  |  ★★★ challenge
-- 
-- Loans originated on a month-end day (the 28th-31st) in 2025 AND over $700,000 OR with LVR
-- above 95. Careful with brackets: `(amount > 700000 OR lvr > 95)` is the second condition.
-- Return `loan_id`, `origination_date`; sorted by `loan_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 495 row(s). Sort the output as described.
-- ============================================================================


SELECT loan_id, origination_date
FROM loan 
WHERE EXTRACT(DAY FROM origination_date) IN (28, 29, 30, 31)
AND EXTRACT(YEAR FROM origination_date) = 2025
  AND (lvr_at_origination_pct > 95 OR original_amount > 700000)
ORDER BY loan_id ASC;
