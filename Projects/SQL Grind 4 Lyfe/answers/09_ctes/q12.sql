-- ============================================================================
-- 09_ctes  |  Q12  |  ★★★ challenge
-- 
-- Refinance chains with recursion: starting from loans with no parent (`parent_loan_id IS
-- NULL`) that have at least one internal-refinance child, follow the child links. Return
-- `chain_length`, `chains`, where chain_length is the number of loans in the chain from the
-- root to the last descendant. Sorted by `chain_length`.
-- 
-- Return 2 column(s), in the order the question gives them.
-- Expected 3 row(s). Sort the output as described.
-- ============================================================================


