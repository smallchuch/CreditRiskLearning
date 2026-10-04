-- ============================================================================
-- cr03_roll_rates  |  Q10  |  ★★★ challenge
-- 
-- Re-default: loans that were 90+ DPD, later reached 0 DPD (cured), then went 30+ again.
-- Count such loans. One number. Hint: self-join snapshots by loan and ordered months (e.g.
-- three `EXISTS` with increasing `months_on_book`).
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


