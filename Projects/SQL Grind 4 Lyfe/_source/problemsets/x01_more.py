from ._gen import *
MORE_FOR = '01_select_filter_sort'
PROBLEMS = []
for p in EXT_PURPOSES:
    PROBLEMS.append(P(1, f"Loans with purpose `'{p}'` originated in 2023 with an original amount over $500,000: return `loan_id`, `original_amount`; largest first, ties by `loan_id`; top 10 only.",
      f"SELECT loan_id, original_amount FROM loan WHERE purpose = '{p}' AND {yr('origination_date',2023)} AND original_amount > 500000 ORDER BY original_amount DESC, loan_id LIMIT 10"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Active loans written through the `'{c}'` channel with an origination LVR above 85: `loan_id`, `lvr_at_origination_pct`; highest LVR first, ties by `loan_id`; top 10.",
      f"SELECT loan_id, lvr_at_origination_pct FROM loan WHERE channel='{c}' AND loan_status='Active' AND lvr_at_origination_pct > 85 ORDER BY lvr_at_origination_pct DESC, loan_id LIMIT 10"))
for s in ['NSW','VIC','QLD','SA','WA']:
    PROBLEMS.append(P(1, f"Branches in `'{s}'`: `branch_id`, `branch_name`, `region`; sorted by `branch_name`.",
      f"SELECT branch_id, branch_name, region FROM dim_branch WHERE state='{s}' ORDER BY branch_name"))
for s in ['NSW','VIC','QLD','SA','WA']:
    PROBLEMS.append(P(1, f"Postcodes in `'{s}'` (`dim_postcode`): `postcode`, `suburb`, `market_segment`; sorted by `postcode`.",
      f"SELECT postcode, suburb, market_segment FROM dim_postcode WHERE state='{s}' ORDER BY postcode"))
for y in YEARS:
    PROBLEMS.append(P(2, f"The 5 loans with the highest `interest_rate_at_origination_pct` originated in {y}: `loan_id`, `interest_rate_at_origination_pct`; highest first, ties by `loan_id`.",
      f"SELECT loan_id, interest_rate_at_origination_pct FROM loan WHERE {yr('origination_date',y)} ORDER BY interest_rate_at_origination_pct DESC, loan_id LIMIT 5"))
for st in ['Settled','Declined','Withdrawn','Lapsed','In Progress','Approved - Awaiting Settlement']:
    PROBLEMS.append(P(2, f"Applications lodged in 2025 with `current_status = '{st}'` and a requested amount over $400,000: `application_id`, `requested_amount`; largest first, ties by `application_id`; top 10.",
      f"SELECT application_id, requested_amount FROM loan_application WHERE current_status='{st}' AND {yr('application_date',2025)} AND requested_amount > 400000 ORDER BY requested_amount DESC, application_id LIMIT 10"))
PROBLEMS += [
 P(3, "Loans originated on a month-end day (the 28th-31st) in 2025 AND over $700,000 OR with LVR above 95. Careful with brackets: `(amount > 700000 OR lvr > 95)` is the second condition. Return `loan_id`, `origination_date`; sorted by `loan_id`.",
   "SELECT loan_id, origination_date FROM loan WHERE origination_date >= DATE '2025-01-01' AND day(origination_date) >= 28 AND (original_amount > 700000 OR lvr_at_origination_pct > 95) ORDER BY loan_id"),
 P(3, "Distinct combinations of `channel` and `purpose` for loans originated in 2025: sorted by `channel`, `purpose`.",
   "SELECT DISTINCT channel, purpose FROM loan WHERE origination_date >= DATE '2025-01-01' ORDER BY 1,2"),
 P(3, "Skip the first 20 and take the next 10: loans ordered by `original_amount` descending, `loan_id` ascending - return `loan_id`, `original_amount` for ranks 21-30 (use `OFFSET`).",
   "SELECT loan_id, original_amount FROM loan ORDER BY original_amount DESC, loan_id LIMIT 10 OFFSET 20"),
]
