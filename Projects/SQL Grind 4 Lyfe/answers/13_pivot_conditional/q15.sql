-- ============================================================================
-- 13_pivot_conditional  |  Q15  |  ★★★ challenge
-- 
-- Complaints per category by year as a pivot using DuckDB `PIVOT` on `year(received_date)`
-- with counts. Return `category` and one column per year ordered ascending; sorted by
-- `category`. Cast the year to text in a subquery first: `SELECT category,
-- CAST(year(received_date) AS VARCHAR) AS yr FROM complaint`.
-- 
-- Return 9 column(s), in the order the question gives them.
-- Expected 8 row(s). Sort the output as described.
-- ============================================================================


