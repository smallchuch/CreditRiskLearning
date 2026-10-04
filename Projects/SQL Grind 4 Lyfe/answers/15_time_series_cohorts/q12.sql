-- ============================================================================
-- 15_time_series_cohorts  |  Q12  |  ★★★ challenge
-- 
-- Cumulative ever-30+ by vintage. For loans originated in 2022, compute at MOB 6, 12, 18, 24
-- the % of loans that have EVER been 30+ DPD up to that MOB (`MAX(days_past_due)>=30` among
-- snapshots with `months_on_book <= k`). Return `mob`, `loans`, `ever_30plus_pct` (2dp) for
-- k in (6,12,18,24); sorted by `mob`. Loans = those 2022 loans that have a snapshot at that
-- MOB.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 4 row(s). Sort the output as described.
-- ============================================================================


