-- ============================================================================
-- 03_nulls  |  Q21  |  ★★★ challenge
-- 
-- Build a single 'bureau quality' label with CASE: `'Thin file'` when `bureau_score IS
-- NULL`, `'Adverse'` when `bankruptcy_flag` or `court_judgements > 0`, `'Weak'` when score <
-- 600, `'Fair'` when 600-749, else `'Strong'`. Return `quality`, `reports` ordered by
-- `reports` descending, then `quality`. Order of the CASE branches matters.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 5 row(s). Sort the output as described.
-- ============================================================================


