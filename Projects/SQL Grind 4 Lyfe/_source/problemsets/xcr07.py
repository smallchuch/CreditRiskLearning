from ._gen import *
MORE_FOR = 'cr07_collateral_lvr'
PROBLEMS = []
QS = ['2024-03-31','2024-06-30','2024-09-30','2024-12-31','2025-03-31','2025-06-30','2025-09-30','2025-12-31']
for d in QS:
    PROBLEMS.append(P(2, f"At {d}: the share of EAD (2 dp %) with `current_lvr_pct` above 80, and above 90 (from `ecl_provision_quarterly`). `pct_gt80`, `pct_gt90`.",
      f"SELECT ROUND(100*SUM(ead) FILTER (WHERE current_lvr_pct>80)/SUM(ead),2), ROUND(100*SUM(ead) FILTER (WHERE current_lvr_pct>90)/SUM(ead),2) FROM ecl_provision_quarterly WHERE reporting_date=DATE '{d}'"))
for p in EXT_PURPOSES:
    PROBLEMS.append(P(2, f"Purpose `'{p}'` at 2025-12-31: EAD-weighted average current LVR (1 dp) and the number of loans above 90% current LVR. `wtd_lvr`, `loans_gt90`.",
      f"SELECT ROUND(SUM(e.current_lvr_pct*e.ead)/SUM(e.ead),1), COUNT(*) FILTER (WHERE e.current_lvr_pct>90) FROM ecl_provision_quarterly e JOIN loan l USING (loan_id) WHERE e.reporting_date=DATE '2025-12-31' AND l.purpose='{p}'"))
for s in STATES:
    PROBLEMS.append(P(3, f"Property state `'{s}'` at 2025-12-31: EAD-weighted current LVR (1 dp), loans over 80% current LVR and their EAD (0 dp). `wtd_lvr`, `loans_gt80`, `ead_gt80`.",
      f"SELECT ROUND(SUM(e.current_lvr_pct*e.ead)/SUM(e.ead),1), COUNT(*) FILTER (WHERE e.current_lvr_pct>80), ROUND(SUM(e.ead) FILTER (WHERE e.current_lvr_pct>80),0) FROM ecl_provision_quarterly e JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE e.reporting_date=DATE '2025-12-31' AND d.state='{s}'"))
for f in (10,20,30):
    PROBLEMS.append(P(3, f"Price-fall scenario -{f}%: at 2025-12-31, loans with stressed current LVR (`current_lvr_pct / {1-f/100}`) above 100 - count and EAD (0 dp). `loans`, `ead`.",
      f"SELECT COUNT(*), ROUND(SUM(ead),0) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND current_lvr_pct/{1-f/100}>100"))
for t in ['Origination - Full Valuation','Origination - Desktop','Automated Valuation (AVM)','Default Revaluation - Full']:
    PROBLEMS.append(P(2, f"Valuation type `'{t}'`: number of valuations, average amount (0 dp), and the count of zero-amount rows. `valuations`, `avg_amount`, `zeros`.",
      f"SELECT COUNT(*), ROUND(AVG(valuation_amount),0), COUNT(*) FILTER (WHERE valuation_amount=0) FROM property_valuation WHERE valuation_type='{t}'"))
