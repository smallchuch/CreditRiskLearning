from ._gen import *
MORE_FOR = '02_expressions_case_functions'
PROBLEMS = []
for p in EXT_PURPOSES:
    PROBLEMS.append(P(1, f"For the 8 largest loans with purpose `'{p}'` (ties by `loan_id`), show `loan_id`, `original_amount` and the first-year interest at the origination rate: `original_amount * rate / 100` rounded to 2 dp. Largest first.",
      f"SELECT loan_id, original_amount, ROUND(original_amount*interest_rate_at_origination_pct/100,2) FROM loan WHERE purpose='{p}' ORDER BY original_amount DESC, loan_id LIMIT 8"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Size-band the `'{c}'` loans originated in 2025 with CASE: `'Small'` under 400,000, `'Mid'` 400,000 to 799,999.99, `'Large'` 800,000 and over. Return `band`, `loans`; sorted by `band`.",
      f"SELECT CASE WHEN original_amount < 400000 THEN 'Small' WHEN original_amount < 800000 THEN 'Mid' ELSE 'Large' END AS band, COUNT(*) FROM loan WHERE channel='{c}' AND {yr('origination_date',2025)} GROUP BY 1 ORDER BY 1"))
STR = [
 ("the surname in upper case (`UPPER`)", "UPPER(last_name)"),
 ("the length of the surname (`LENGTH`)", "LENGTH(last_name)"),
 ("the first three letters of the first name (`LEFT`)", "LEFT(first_name,3)"),
 ("`last_name, first_name` joined as one text value (`||`)", "last_name || ', ' || first_name"),
 ("initials (first letter of first name then first letter of surname)", "LEFT(first_name,1) || LEFT(last_name,1)"),
 ("the email domain - everything after the `@` (use `SPLIT_PART(email,'@',2)`)", "SPLIT_PART(email,'@',2)"),
 ("the email in lower case with spaces trimmed", "LOWER(TRIM(email))"),
 ("the mobile with all spaces removed (`REPLACE`)", "REPLACE(mobile,' ','')"),
]
for i,(d,e) in enumerate(STR):
    PROBLEMS.append(P(1, f"The first 15 customers (by id) that have both an email and a mobile: `customer_id` and {d}. Sorted by `customer_id`.",
      f"SELECT customer_id, {e} FROM customer WHERE customer_id <= 40 AND email IS NOT NULL AND mobile IS NOT NULL ORDER BY customer_id LIMIT 15".replace("customer_id <= 40","customer_id <= 40")))
for t in (180,240,300,360):
    PROBLEMS.append(P(2, f"Monthly P&I repayment (2 dp) at the origination rate for loans with a {t}-month term and `loan_id <= 200`, first 8 by `loan_id`: `loan_id`, repayment. Formula `P*r/(1-(1+r)^-n)` with `r = rate/1200`.",
      f"SELECT loan_id, ROUND(original_amount*(interest_rate_at_origination_pct/1200)/(1-POWER(1+interest_rate_at_origination_pct/1200,-term_months)),2) FROM loan WHERE term_months={t} AND loan_id <= 400 ORDER BY loan_id LIMIT 8"))
MATH = [("rounded to the nearest $10,000 (`ROUND(x,-4)`)", "ROUND(original_amount,-4)"), ("rounded UP to the next $50,000 (`CEIL`)", "CEIL(original_amount/50000)*50000"),
        ("rounded DOWN to the previous $50,000 (`FLOOR`)", "FLOOR(original_amount/50000)*50000"), ("the LVR as a fraction (`lvr/100`, 4 dp)", "ROUND(lvr_at_origination_pct/100,4)"),
        ("the loan-to-value shortfall to 80% LVR in dollars: `security_value_at_origination*0.8 - original_amount` (0 dp, may be negative)", "ROUND(security_value_at_origination*0.8-original_amount,0)")]
for d,e in MATH:
    PROBLEMS.append(P(1, f"Loans 1-12: `loan_id` and `original_amount` {d}. Sorted by `loan_id`." if 'shortfall' not in d and 'fraction' not in d else f"Loans 1-12: `loan_id` and {d}. Sorted by `loan_id`.",
      f"SELECT loan_id, {e} FROM loan WHERE loan_id <= 12 ORDER BY loan_id"))
PROBLEMS += [
 P(2, "Nested CASE: label loans 1-30 `'Prime owner-occ'` if `purpose = 'Purchase - Owner Occupied'` AND LVR <= 80; `'High-LVR owner-occ'` if owner-occupied and LVR > 80; `'Investor'` if `'Purchase - Investment'`; else `'Other'`. Return `loan_id`, `label`; sorted by `loan_id`.",
   "SELECT loan_id, CASE WHEN purpose='Purchase - Owner Occupied' AND lvr_at_origination_pct<=80 THEN 'Prime owner-occ' WHEN purpose='Purchase - Owner Occupied' THEN 'High-LVR owner-occ' WHEN purpose='Purchase - Investment' THEN 'Investor' ELSE 'Other' END FROM loan WHERE loan_id<=30 ORDER BY loan_id"),
 P(3, "`GREATEST` / `LEAST`: for loans 1-12 return `loan_id` and `GREATEST(original_amount, security_value_at_origination*0.5)` and `LEAST(original_amount, 600000)`. Sorted by `loan_id`.",
   "SELECT loan_id, GREATEST(original_amount, security_value_at_origination*0.5), LEAST(original_amount,600000) FROM loan WHERE loan_id<=12 ORDER BY loan_id"),
 P(3, "Integer division and remainder: for loans 1-12 return `loan_id`, `term_months // 12` (whole years) and `term_months % 12` (leftover months). Sorted by `loan_id`.",
   "SELECT loan_id, term_months // 12, term_months % 12 FROM loan WHERE loan_id<=12 ORDER BY loan_id"),
]
