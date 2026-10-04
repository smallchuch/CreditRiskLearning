# CR09 - Losses, LGD and ECL provisioning

`answers/cr09_loss_ecl/qNN.sql` &nbsp;|&nbsp; check with: `grade cr09` or `grade cr09 q03`

Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. Rows only need to be sorted when the question says so. Numbers match within a small tolerance.

## Scenario: how much will we lose, and are we provisioned for it?

```
 Expected Credit Loss  =  PD  x  LGD  x  EAD
   PD  probability of default (12-month for stage 1, lifetime for stage 2/3)
   LGD loss given default (% of exposure lost after selling the property, costs, and LMI)
   EAD exposure at default (balance at default)
```
**IFRS 9 stages**
* Stage 1 - performing: 12-month ECL
* Stage 2 - significant increase in credit risk (e.g. 30+ DPD, hardship): lifetime ECL
* Stage 3 - credit-impaired (90+ DPD, in recovery): lifetime ECL on a defaulted loan

Tables: `ecl_provision_quarterly` (stage, pd_12m, pd_lifetime, lgd, ead, ecl_amount, stage_reason per loan per quarter-end) and `loan_loss` (realised outcome after possession/sale: `shortfall_before_lmi`, `lmi_recovery`, `net_loss`, `lgd_pct`).

**Coverage ratio** = ECL / EAD (provision as % of exposure). Stage 3 should be much higher than Stage 1.
**Stage migration** = how loans move between stages quarter to quarter.

---

## Problems

### Q01 &nbsp; ★ &nbsp; (warm-up)

ECL by stage at 2025-12-31: loans, EAD (0dp), ECL (0dp), coverage % (2dp). `ifrs9_stage`, `loans`, `ead`, `ecl`, `coverage_pct`; sorted by stage.

> Return **5 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q02 &nbsp; ★ &nbsp; (warm-up)

Total ECL (0dp) at each reporting date in 2024-2025. `reporting_date`, `total_ecl`; sorted by date.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **8 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q03 &nbsp; ★ &nbsp; (warm-up)

Realised loss summary from `loan_loss`: number of losses, total EAD at default, total net loss (0dp), and average LGD % (1dp). `losses`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q04 &nbsp; ★★ &nbsp; (core)

Stage reasons: for Stage 2 loans at 2025-12-31, the count by `stage_reason`. `stage_reason`, `loans`; sorted by loans descending then reason.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q05 &nbsp; ★★ &nbsp; (core)

EAD-weighted average PD (12m, 4dp as fraction) and LGD (4dp) by stage at 2025-12-31. `ifrs9_stage`, `wtd_pd12`, `wtd_lgd`; sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q06 &nbsp; ★★ &nbsp; (core)

Realised LGD by origination LVR band bucket (`<=80`, `80-90`, `>90`) for loans in `loan_loss` (join `loan`): count and average `lgd_pct` (1dp). `lvr_bucket`, `losses`, `avg_lgd_pct`; sorted by bucket label.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q07 &nbsp; ★★ &nbsp; (core)

LMI effect: total shortfall before LMI and total LMI recovery (0dp) in `loan_loss`, and net loss; show the % of the shortfall recovered by LMI (1dp). `shortfall`, `lmi_recovery`, `net_loss`, `lmi_recovery_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q08 &nbsp; ★★★ &nbsp; (challenge)

Stage migration Sep-30-2025 -> Dec-31-2025: a transition matrix of loan counts. `from_stage`, `to_stage`, `loans`; sorted by from, to. Include loans present in both quarters.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **9 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q09 &nbsp; ★★★ &nbsp; (challenge)

Provision build: ECL change by stage from 2025-09-30 to 2025-12-31 (total ECL by stage each date, 0dp, and difference). `ifrs9_stage`, `ecl_sep`, `ecl_dec`, `change`; sorted by stage.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q10 &nbsp; ★★★ &nbsp; (challenge)

Back-test: for loans that defaulted (in `loan_loss`), what was their stage 4 quarters before `default_date`? Use the latest reporting_date <= default_date - 1 year. Count by stage. `ifrs9_stage`, `loans`; sorted by stage. (Were we early enough?)

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **2 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q11 &nbsp; ★★★ &nbsp; (challenge)

Check the ECL arithmetic: count loan-quarters at 2025-12-31 where `ecl_amount` differs from `ead * lgd * (pd_12m for stage 1, pd_lifetime for stage 2/3)` by more than $1. One number. (Information check; may be non-zero because of model overlays.)

> Return **1 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q12 &nbsp; ★★★ &nbsp; (challenge)

Loss timeline: time from `default_date` to `sale_date` in months (median, 1dp) and from default to `possession_date`. `median_default_to_possession_m`, `median_default_to_sale_m`. Use `date_diff('day', ...)/30.44`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q13 &nbsp; ★★★ &nbsp; (challenge)

Sale shortfall analysis: loans where `sale_price` < `balance_at_sale` (a shortfall); count and % of all loans in `loan_loss` (1dp). `shortfall_loans`, `pct`.

> Return **2 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q14 &nbsp; ★★ &nbsp; (core)

ECL at 2024-03-31: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q15 &nbsp; ★★ &nbsp; (core)

ECL at 2024-06-30: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q16 &nbsp; ★★ &nbsp; (core)

ECL at 2024-09-30: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q17 &nbsp; ★★ &nbsp; (core)

ECL at 2024-12-31: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q18 &nbsp; ★★ &nbsp; (core)

ECL at 2025-03-31: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q19 &nbsp; ★★ &nbsp; (core)

ECL at 2025-06-30: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q20 &nbsp; ★★ &nbsp; (core)

ECL at 2025-09-30: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q21 &nbsp; ★★ &nbsp; (core)

ECL at 2025-12-31: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q22 &nbsp; ★★★ &nbsp; (challenge)

Property state `'NSW'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q23 &nbsp; ★★★ &nbsp; (challenge)

Property state `'VIC'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q24 &nbsp; ★★★ &nbsp; (challenge)

Property state `'QLD'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q25 &nbsp; ★★★ &nbsp; (challenge)

Property state `'SA'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q26 &nbsp; ★★★ &nbsp; (challenge)

Property state `'WA'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q27 &nbsp; ★★★ &nbsp; (challenge)

Property state `'TAS'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q28 &nbsp; ★★★ &nbsp; (challenge)

Property state `'NT'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q29 &nbsp; ★★★ &nbsp; (challenge)

Property state `'ACT'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q30 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Purchase - Owner Occupied'` at 2025-12-31: ECL coverage (2 dp %) by IFRS 9 stage. `ifrs9_stage`, `loans`, `coverage_pct`; sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q31 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Purchase - Investment'` at 2025-12-31: ECL coverage (2 dp %) by IFRS 9 stage. `ifrs9_stage`, `loans`, `coverage_pct`; sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q32 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Refinance'` at 2025-12-31: ECL coverage (2 dp %) by IFRS 9 stage. `ifrs9_stage`, `loans`, `coverage_pct`; sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q33 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Equity Release / Top-up'` at 2025-12-31: ECL coverage (2 dp %) by IFRS 9 stage. `ifrs9_stage`, `loans`, `coverage_pct`; sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q34 &nbsp; ★★★ &nbsp; (challenge)

Purpose `'Construction'` at 2025-12-31: ECL coverage (2 dp %) by IFRS 9 stage. `ifrs9_stage`, `loans`, `coverage_pct`; sorted by stage.

> Return **3 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **3 row(s)** &nbsp;|&nbsp; Sort the output as described.

### Q35 &nbsp; ★★ &nbsp; (core)

Defaults in 2019: loans in `loan_loss` with `default_date` in 2019 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q36 &nbsp; ★★ &nbsp; (core)

Defaults in 2020: loans in `loan_loss` with `default_date` in 2020 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q37 &nbsp; ★★ &nbsp; (core)

Defaults in 2021: loans in `loan_loss` with `default_date` in 2021 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q38 &nbsp; ★★ &nbsp; (core)

Defaults in 2022: loans in `loan_loss` with `default_date` in 2022 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q39 &nbsp; ★★ &nbsp; (core)

Defaults in 2023: loans in `loan_loss` with `default_date` in 2023 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q40 &nbsp; ★★ &nbsp; (core)

Defaults in 2024: loans in `loan_loss` with `default_date` in 2024 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.

### Q41 &nbsp; ★★ &nbsp; (core)

Defaults in 2025: loans in `loan_loss` with `default_date` in 2025 - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.

> Return **4 column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **1 row(s)** &nbsp;|&nbsp; Row order does not matter.
