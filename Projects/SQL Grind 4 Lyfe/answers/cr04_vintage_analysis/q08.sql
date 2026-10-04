-- ============================================================================
-- cr04_vintage_analysis  |  Q08  |  ★★★ challenge
-- 
-- Bureau score at origination vs later default: bucket the primary applicant's
-- `bureau_score` at application (join via `loan.application_id` to `credit_bureau_report`
-- for the primary customer) into `<600`, `600-699`, `700-799`, `800+`, with NULLs as `no
-- score`; return the ever-90+ rate (2dp) per bucket. `score_band`, `loans`, `ever90_pct`;
-- sorted by band label alphabetically.
-- 
-- Return 3 column(s), in the order the question gives them.
-- Expected 5 row(s). Sort the output as described.
-- ============================================================================


