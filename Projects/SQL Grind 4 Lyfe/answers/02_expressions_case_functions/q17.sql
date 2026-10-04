-- ============================================================================
-- 02_expressions_case_functions  |  Q17  |  ★★ core
-- 
-- Does `assessed_living_expenses` always equal the greater of declared expenses and the HEM
-- benchmark? Join-free check inside `application_assessment` won't have declared expenses,
-- so instead verify: count rows where `hem_applied_flag` is true but
-- `assessed_living_expenses` <> `hem_benchmark_monthly`. One number.
-- 
-- Return 1 column(s), in the order the question gives them.
-- Expected 1 row(s). Row order does not matter.
-- ============================================================================


