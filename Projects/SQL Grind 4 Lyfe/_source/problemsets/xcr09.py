from ._gen import *
MORE_FOR = 'cr09_loss_ecl'
PROBLEMS = []
QS = ['2024-03-31','2024-06-30','2024-09-30','2024-12-31','2025-03-31','2025-06-30','2025-09-30','2025-12-31']
for d in QS:
    PROBLEMS.append(P(2, f"ECL at {d}: total EAD (0 dp), total ECL (0 dp), coverage (2 dp %), and Stage 2+3 share of EAD (2 dp %). `ead`, `ecl`, `coverage_pct`, `stage23_pct`.",
      f"SELECT ROUND(SUM(ead),0), ROUND(SUM(ecl_amount),0), ROUND(100*SUM(ecl_amount)/SUM(ead),2), ROUND(100*SUM(ead) FILTER (WHERE ifrs9_stage>=2)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '{d}'"))
for s in STATES:
    PROBLEMS.append(P(3, f"Property state `'{s}'` at 2025-12-31: loans, EAD (0 dp), ECL (0 dp) and coverage (2 dp %). `loans`, `ead`, `ecl`, `coverage_pct`.",
      f"SELECT COUNT(*), ROUND(SUM(e.ead),0), ROUND(SUM(e.ecl_amount),0), ROUND(100*SUM(e.ecl_amount)/SUM(e.ead),2) FROM ecl_provision_quarterly e JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE e.reporting_date=DATE '2025-12-31' AND d.state='{s}'"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(3, f"Purpose `'{p}'` at 2025-12-31: ECL coverage (2 dp %) by IFRS 9 stage. `ifrs9_stage`, `loans`, `coverage_pct`; sorted by stage.",
      f"SELECT e.ifrs9_stage, COUNT(*), ROUND(100*SUM(e.ecl_amount)/SUM(e.ead),2) FROM ecl_provision_quarterly e JOIN loan l USING (loan_id) WHERE e.reporting_date=DATE '2025-12-31' AND l.purpose='{p}' GROUP BY 1 ORDER BY 1"))
for y in range(2019,2026):
    PROBLEMS.append(P(2, f"Defaults in {y}: loans in `loan_loss` with `default_date` in {y} - count, total EAD at default (0 dp), total net loss (0 dp), average LGD (1 dp %). `defaults`, `ead`, `net_loss`, `avg_lgd_pct`.",
      f"SELECT COUNT(*), ROUND(SUM(ead_at_default),0), ROUND(SUM(net_loss),0), ROUND(AVG(lgd_pct),1) FROM loan_loss WHERE {yr('default_date',y)}"))
