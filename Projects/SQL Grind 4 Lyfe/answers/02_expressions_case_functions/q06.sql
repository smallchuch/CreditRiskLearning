-- ============================================================================
-- 02_expressions_case_functions  |  Q06  |  ★★ core
-- 
-- Label each product `Fixed`/`Variable` plus term: return `product_id` and a label like
-- `Fixed 24m` or `Variable` (for variable products). Sorted by `product_id`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 15 row(s). Sort the output as described.
-- ============================================================================


SELECT 
        product_id,
        CASE 
            WHEN rate_type = 'Fixed' THEN CONCAT(rate_type, ' ', fixed_term_months, 'm')
            WHEN rate_type = 'Variable' THEN rate_type
            ELSE 'Other'
        END AS fixed_variable
FROM dim_product;