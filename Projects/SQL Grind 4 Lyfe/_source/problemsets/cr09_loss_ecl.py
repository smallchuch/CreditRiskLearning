from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="cr09_loss_ecl", title="CR09 - Losses, LGD and ECL provisioning", primer=PRIMER, problems=[
    P(1, "ECL by stage at 2025-12-31: loans, EAD (0dp), ECL (0dp), coverage % (2dp). `ifrs9_stage`, `loans`, `ead`, `ecl`, `coverage_pct`; sorted by stage.",
      "SELECT ifrs9_stage, COUNT(*), ROUND(SUM(ead),0), ROUND(SUM(ecl_amount),0), ROUND(100*SUM(ecl_amount)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' GROUP BY 1 ORDER BY 1"),
    P(1, "Total ECL (0dp) at each reporting date in 2024-2025. `reporting_date`, `total_ecl`; sorted by date.",
      "SELECT reporting_date, ROUND(SUM(ecl_amount),0) FROM ecl_provision_quarterly WHERE reporting_date>=DATE '2024-01-01' GROUP BY 1 ORDER BY 1"),
    P(1, "Realised loss summary from `loan_loss`: number of losses, total EAD at default, total net loss (0dp), and average LGD % (1dp). `losses`, `ead`, `net_loss`, `avg_lgd_pct`.",
      "SELECT COUNT(*), ROUND(SUM(ead_at_default),0), ROUND(SUM(net_loss),0), ROUND(AVG(lgd_pct),1) FROM loan_loss"),
    P(2, "Stage reasons: for Stage 2 loans at 2025-12-31, the count by `stage_reason`. `stage_reason`, `loans`; sorted by loans descending then reason.",
      "SELECT stage_reason, COUNT(*) AS n FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND ifrs9_stage=2 GROUP BY 1 ORDER BY n DESC, 1"),
    P(2, "EAD-weighted average PD (12m, 4dp as fraction) and LGD (4dp) by stage at 2025-12-31. `ifrs9_stage`, `wtd_pd12`, `wtd_lgd`; sorted by stage.",
      "SELECT ifrs9_stage, ROUND(SUM(pd_12m*ead)/SUM(ead),4), ROUND(SUM(lgd*ead)/SUM(ead),4) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' GROUP BY 1 ORDER BY 1"),
    P(2, "Realised LGD by origination LVR band bucket (`<=80`, `80-90`, `>90`) for loans in `loan_loss` (join `loan`): count and average `lgd_pct` (1dp). `lvr_bucket`, `losses`, `avg_lgd_pct`; sorted by bucket label.",
      "SELECT CASE WHEN l.lvr_at_origination_pct<=80 THEN '<=80' WHEN l.lvr_at_origination_pct<=90 THEN '80-90' ELSE '>90' END AS b, COUNT(*), ROUND(AVG(x.lgd_pct),1) FROM loan_loss x JOIN loan l USING (loan_id) GROUP BY 1 ORDER BY 1"),
    P(2, "LMI effect: total shortfall before LMI and total LMI recovery (0dp) in `loan_loss`, and net loss; show the % of the shortfall recovered by LMI (1dp). `shortfall`, `lmi_recovery`, `net_loss`, `lmi_recovery_pct`.",
      "SELECT ROUND(SUM(shortfall_before_lmi),0), ROUND(SUM(lmi_recovery),0), ROUND(SUM(net_loss),0), ROUND(100*SUM(lmi_recovery)/SUM(shortfall_before_lmi),1) FROM loan_loss"),
    P(3, "Stage migration Sep-30-2025 -> Dec-31-2025: a transition matrix of loan counts. `from_stage`, `to_stage`, `loans`; sorted by from, to. Include loans present in both quarters.",
      "SELECT a.ifrs9_stage, b.ifrs9_stage, COUNT(*) FROM ecl_provision_quarterly a JOIN ecl_provision_quarterly b ON b.loan_id=a.loan_id AND b.reporting_date=DATE '2025-12-31' WHERE a.reporting_date=DATE '2025-09-30' GROUP BY 1,2 ORDER BY 1,2"),
    P(3, "Provision build: ECL change by stage from 2025-09-30 to 2025-12-31 (total ECL by stage each date, 0dp, and difference). `ifrs9_stage`, `ecl_sep`, `ecl_dec`, `change`; sorted by stage.",
      "SELECT ifrs9_stage, ROUND(SUM(ecl_amount) FILTER (WHERE reporting_date=DATE '2025-09-30'),0), ROUND(SUM(ecl_amount) FILTER (WHERE reporting_date=DATE '2025-12-31'),0), ROUND(SUM(ecl_amount) FILTER (WHERE reporting_date=DATE '2025-12-31')-SUM(ecl_amount) FILTER (WHERE reporting_date=DATE '2025-09-30'),0) FROM ecl_provision_quarterly WHERE reporting_date IN (DATE '2025-09-30', DATE '2025-12-31') GROUP BY 1 ORDER BY 1"),
    P(3, "Back-test: for loans that defaulted (in `loan_loss`), what was their stage 4 quarters before `default_date`? Use the latest reporting_date <= default_date - 1 year. Count by stage. `ifrs9_stage`, `loans`; sorted by stage. (Were we early enough?)",
      "SELECT e.ifrs9_stage, COUNT(*) FROM loan_loss x JOIN ecl_provision_quarterly e ON e.loan_id=x.loan_id WHERE e.reporting_date = (SELECT MAX(e2.reporting_date) FROM ecl_provision_quarterly e2 WHERE e2.loan_id=x.loan_id AND e2.reporting_date <= x.default_date - INTERVAL 1 YEAR) GROUP BY 1 ORDER BY 1"),
    P(3, "Check the ECL arithmetic: count loan-quarters at 2025-12-31 where `ecl_amount` differs from `ead * lgd * (pd_12m for stage 1, pd_lifetime for stage 2/3)` by more than $1. One number. (Information check; may be non-zero because of model overlays.)",
      "SELECT COUNT(*) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND ABS(ecl_amount - ead*lgd*CASE WHEN ifrs9_stage=1 THEN pd_12m ELSE pd_lifetime END) > 1"),
    P(3, "Loss timeline: time from `default_date` to `sale_date` in months (median, 1dp) and from default to `possession_date`. `median_default_to_possession_m`, `median_default_to_sale_m`. Use `date_diff('day', ...)/30.44`.",
      "SELECT ROUND(MEDIAN(date_diff('day', default_date, possession_date)/30.44),1), ROUND(MEDIAN(date_diff('day', default_date, sale_date)/30.44),1) FROM loan_loss"),
    P(3, "Sale shortfall analysis: loans where `sale_price` < `balance_at_sale` (a shortfall); count and % of all loans in `loan_loss` (1dp). `shortfall_loans`, `pct`.",
      "SELECT COUNT(*) FILTER (WHERE sale_price<balance_at_sale), ROUND(100.0*COUNT(*) FILTER (WHERE sale_price<balance_at_sale)/COUNT(*),1) FROM loan_loss"),
])
