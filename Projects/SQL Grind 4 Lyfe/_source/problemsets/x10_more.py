from ._gen import *
MORE_FOR = '10_window_ranking'
PROBLEMS = []
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"For `'{p}'` loans: the 2 largest loans in each `channel` (ties by `loan_id`). `channel`, `loan_id`, `original_amount`, `rn`; sorted by channel, rn.",
      f"SELECT channel, loan_id, original_amount, rn FROM (SELECT channel, loan_id, original_amount, ROW_NUMBER() OVER (PARTITION BY channel ORDER BY original_amount DESC, loan_id) AS rn FROM loan WHERE purpose='{p}') WHERE rn<=2 ORDER BY channel, rn"))
for y in YEARS:
    PROBLEMS.append(P(2, f"Rank products by number of loans originated in {y} using `RANK()`; return the top 3 (ties may add rows). `product_id`, `loans`, `rnk`; sorted by rnk, product_id.",
      f"SELECT * FROM (SELECT product_id, COUNT(*) AS n, RANK() OVER (ORDER BY COUNT(*) DESC) AS r FROM loan WHERE {yr('origination_date',y)} GROUP BY 1) WHERE r<=3 ORDER BY r, product_id"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Quartiles of `'{c}'` loan amounts: `NTILE(4)` over `original_amount` (tie `loan_id`); return per quartile the loan count, min and max amount. `quartile`, `loans`, `min_amount`, `max_amount`; sorted by quartile.",
      f"SELECT q, COUNT(*), MIN(original_amount), MAX(original_amount) FROM (SELECT original_amount, NTILE(4) OVER (ORDER BY original_amount, loan_id) AS q FROM loan WHERE channel='{c}') GROUP BY 1 ORDER BY 1"))
for s in ['NSW','VIC','QLD','SA','WA']:
    PROBLEMS.append(P(3, f"Dense rank branches in `'{s}'` by loans originated (most = 1); show ranks 1-3. `branch_name`, `loans`, `drnk`; sorted by drnk, branch_name.",
      f"SELECT * FROM (SELECT b.branch_name, COUNT(*) AS n, DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS r FROM loan l JOIN dim_branch b USING (branch_id) WHERE b.state='{s}' GROUP BY b.branch_id, b.branch_name) WHERE r<=3 ORDER BY r, branch_name"))
for y in (2020,2022,2024):
    PROBLEMS.append(P(3, f"Each customer's most recent application up to the end of {y} (latest `application_date`, tie `application_id`): count how many of those latest applications were `'Declined'`. One number.",
      f"SELECT COUNT(*) FROM (SELECT decision FROM loan_application WHERE application_date < DATE '{y+1}-01-01' QUALIFY ROW_NUMBER() OVER (PARTITION BY primary_customer_id ORDER BY application_date DESC, application_id DESC)=1) WHERE decision='Declined'"))
for k in (1,3,5):
    PROBLEMS.append(P(3, f"Top {k} per `purpose`: the {k} loans with the highest `lvr_at_origination_pct` in each purpose (ties by `loan_id`). Return `purpose`, `loan_id`, `lvr_at_origination_pct`; sorted by purpose, then LVR descending, then loan_id.",
      f"SELECT purpose, loan_id, lvr_at_origination_pct FROM loan QUALIFY ROW_NUMBER() OVER (PARTITION BY purpose ORDER BY lvr_at_origination_pct DESC, loan_id) <= {k} ORDER BY purpose, lvr_at_origination_pct DESC, loan_id"))
for y in (2021,2023,2025):
    PROBLEMS.append(P(2, f"Percentile rank of loans originated in {y}: the 5 loans with the highest `PERCENT_RANK()` by original amount (ties by loan_id). `loan_id`, `original_amount`, `pct_rank` (4 dp).",
      f"SELECT loan_id, original_amount, ROUND(pr,4) FROM (SELECT loan_id, original_amount, PERCENT_RANK() OVER (ORDER BY original_amount) AS pr FROM loan WHERE {yr('origination_date',y)}) ORDER BY original_amount DESC, loan_id LIMIT 5"))
