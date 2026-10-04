# CR07 - Collateral, current LVR and valuations

`answers/cr07_collateral_lvr/qNN.sql` &nbsp;|&nbsp; check with: `grade cr07` or `grade cr07 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: what is the security worth now?

Origination LVR is a *historic* number. Risk teams revalue the security: **current LVR = balance / current property value**.

```
 balance $450k / value at origination $600k  = 75% LVR      (then)
 balance $430k / value now          $480k    = 90% LVR      (after a 20% house price fall)
```
Sources of value:
* `property_valuation` (several rows per property: Origination - Full / Desktop, AVM, Default Revaluation) - **AVM = automated valuation**; zeros are bad data.
* `ref_property_price_index` (HPI by state and month-end) to index a value forward or back.
* `ecl_provision_quarterly.current_lvr_pct` - the bank's own stored current LVR.
* `loan_security` holds the property link, cross-collateral (several securities) and `allocated_value`.

LMI (lender's mortgage insurance) covers shortfalls on high-LVR loans (`lmi_flag`).

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

Valuation types: count of valuation rows per `valuation_type`. `valuation_type`, `rows`; sorted by rows descending.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Origination LVR bands (use `ref_lvr_band`, lower exclusive/upper inclusive, first band incl. 0): count of loans per band. `band_name`, `loans`; sorted by band_id.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **6 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

LMI coverage: % of loans with `lmi_flag` among loans with origination LVR above 80 (2dp). One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Current LVR distribution from the ECL table at 2025-12-31: count and balance (EAD, 0dp) in bands `<=60`, `60-80`, `80-90`, `>90` (upper inclusive). `band`, `loans`, `ead`; sorted by band lower bound.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **4 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

Latest non-zero AVM per property: how many properties have a latest AVM (`valuation_type` 'Automated Valuation (AVM)', amount > 0, date <= 2025-12-31)? One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q06 &nbsp; ★★ &nbsp; (core)

Cross-collateral: loans with more than one security and their number of securities, with total `allocated_value` (0dp). Show the 10 largest by total allocated value. `loan_id`, `securities`, `total_allocated`; sorted by total descending then id.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **10 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

Does the stored security value tie back? For loans, compare `security_value_at_origination` with the sum of `allocated_value` across `loan_security`: count loans where they differ by more than $1. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Indexed current LVR: for live loans at 2025-12-31 estimate property value now = `security_value_at_origination` * (HPI of the property's state at 2025-12-31 / HPI at the origination month-end). Then current LVR = balance / value. Return the % of live loans with indexed LVR above 80 (2dp) and above 100 (2dp). `pct_gt80`, `pct_gt100`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

Price fall scenario: a 20% fall in property values. Using `ecl_provision_quarterly` at 2025-12-31 (`ead`, `current_lvr_pct`), the number of loans and EAD (0dp) where the stressed LVR (`current_lvr_pct / 0.8`) exceeds 100. `loans`, `ead`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

AVM zero problem: how many live loans (at 2025-12-31) have a property whose most recent valuation row (by date, valuation_id) is an AVM with amount 0? These would break an LVR calculation. One number.

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Valuation shift between origination and now for the same property (latest non-zero AVM vs `security_value_at_origination`): the average % change (1dp) per property state, for loans with such an AVM. `state`, `avg_change_pct`; sorted by state.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Negative equity watch: loans in the ECL table at 2025-12-31 with `current_lvr_pct > 100`, by stage. `ifrs9_stage`, `loans`, `ead` (0dp); sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q13 &nbsp; ★★ &nbsp; (core)

At 2024-03-31: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★ &nbsp; (core)

At 2024-06-30: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★ &nbsp; (core)

At 2024-09-30: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

At 2024-12-31: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

At 2025-03-31: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

At 2025-06-30: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

At 2025-09-30: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

At 2025-12-31: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Owner Occupied'` at 2025-12-31: EAD-weighted average current LVR (1 dp) and the number of loans above 90% current LVR. `wtd_lvr`, `loans_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★ &nbsp; (core)

Purpose `'Purchase - Investment'` at 2025-12-31: EAD-weighted average current LVR (1 dp) and the number of loans above 90% current LVR. `wtd_lvr`, `loans_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★ &nbsp; (core)

Purpose `'Refinance'` at 2025-12-31: EAD-weighted average current LVR (1 dp) and the number of loans above 90% current LVR. `wtd_lvr`, `loans_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★ &nbsp; (core)

Purpose `'Equity Release / Top-up'` at 2025-12-31: EAD-weighted average current LVR (1 dp) and the number of loans above 90% current LVR. `wtd_lvr`, `loans_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★ &nbsp; (core)

Purpose `'Construction'` at 2025-12-31: EAD-weighted average current LVR (1 dp) and the number of loans above 90% current LVR. `wtd_lvr`, `loans_gt90`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

Property state `'NSW'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

Property state `'VIC'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

Property state `'QLD'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

Property state `'SA'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

Property state `'WA'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q31 &nbsp; ★★★ &nbsp; (challenge)

Property state `'TAS'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q32 &nbsp; ★★★ &nbsp; (challenge)

Property state `'NT'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q33 &nbsp; ★★★ &nbsp; (challenge)

Property state `'ACT'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q34 &nbsp; ★★★ &nbsp; (challenge)

Price-fall scenario -10%: at 2025-12-31, loans with stressed current LVR (`current_lvr_pct / 0.9`) above 100 - count and EAD (0 dp). `loans`, `ead`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q35 &nbsp; ★★★ &nbsp; (challenge)

Price-fall scenario -20%: at 2025-12-31, loans with stressed current LVR (`current_lvr_pct / 0.8`) above 100 - count and EAD (0 dp). `loans`, `ead`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★★ &nbsp; (challenge)

Price-fall scenario -30%: at 2025-12-31, loans with stressed current LVR (`current_lvr_pct / 0.7`) above 100 - count and EAD (0 dp). `loans`, `ead`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★ &nbsp; (core)

Valuation type `'Origination - Full Valuation'`: number of valuations, average amount (0 dp), and the count of zero-amount rows. `valuations`, `avg_amount`, `zeros`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★ &nbsp; (core)

Valuation type `'Origination - Desktop'`: number of valuations, average amount (0 dp), and the count of zero-amount rows. `valuations`, `avg_amount`, `zeros`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★ &nbsp; (core)

Valuation type `'Automated Valuation (AVM)'`: number of valuations, average amount (0 dp), and the count of zero-amount rows. `valuations`, `avg_amount`, `zeros`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★ &nbsp; (core)

Valuation type `'Default Revaluation - Full'`: number of valuations, average amount (0 dp), and the count of zero-amount rows. `valuations`, `avg_amount`, `zeros`.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
