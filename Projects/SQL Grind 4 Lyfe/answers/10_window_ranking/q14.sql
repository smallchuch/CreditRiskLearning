-- ============================================================================
-- 10_window_ranking  |  Q14  |  ★★★ challenge
-- 
-- Keep the cleanest status event: in `application_status_history` some events are duplicated
-- with a later `loaded_at`. For each (`application_id`, `status`) keep the row with the
-- EARLIEST `loaded_at` (tie `event_id`). Count rows after de-duplication. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


