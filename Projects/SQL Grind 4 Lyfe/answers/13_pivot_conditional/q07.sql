-- ============================================================================
-- 13_pivot_conditional  |  Q07  |  ★★ core
-- 
-- LVR band x purpose matrix: for loans, count by LVR band (`<=60`, `60-80`, `80-90`, `>90`
-- using CASE) as columns, per `purpose` as rows. Return `purpose`, `le60`, `b60_80`,
-- `b80_90`, `gt90`; sorted by `purpose`. Upper bounds inclusive (a loan at exactly 80
-- belongs to 60-80).
-- 
-- Return 5 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


