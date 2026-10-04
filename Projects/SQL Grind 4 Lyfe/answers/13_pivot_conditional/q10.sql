-- ============================================================================
-- 13_pivot_conditional  |  Q10  |  ★★★ challenge
-- 
-- Default rate by LVR band. Use `ref_lvr_band` to bucket each loan's
-- `lvr_at_origination_pct` (a band holds LVRs above its `lvr_from_pct` up to and including
-- its `lvr_to_pct`; the first band also includes 0; a NULL upper bound means no cap). For
-- each band return `band_name`, `loans`, `ever_90` (loans that were ever 90+ DPD in any
-- snapshot) and `rate_pct` (2dp). Sorted by `band_id`.
-- 
-- Return 4 column(s), in the order the question gives them.
-- Expected 6 row(s). Sort the output as described.
-- ============================================================================


