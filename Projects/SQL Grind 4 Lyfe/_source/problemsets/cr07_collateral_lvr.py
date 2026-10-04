from . import P

PRIMER = r"""
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
"""

CONCEPT = dict(id="cr07_collateral_lvr", title="CR07 - Collateral, current LVR and valuations", primer=PRIMER, problems=[
    P(1, "Valuation types: count of valuation rows per `valuation_type`. `valuation_type`, `rows`; sorted by rows descending.",
      "SELECT valuation_type, COUNT(*) AS n FROM property_valuation GROUP BY 1 ORDER BY n DESC, 1"),
    P(1, "Origination LVR bands (use `ref_lvr_band`, lower exclusive/upper inclusive, first band incl. 0): count of loans per band. `band_name`, `loans`; sorted by band_id.",
      "SELECT b.band_name, COUNT(*) FROM loan l JOIN ref_lvr_band b ON (l.lvr_at_origination_pct>b.lvr_from_pct OR b.lvr_from_pct=0) AND l.lvr_at_origination_pct<=COALESCE(b.lvr_to_pct,1e9) GROUP BY b.band_id, b.band_name ORDER BY b.band_id"),
    P(1, "LMI coverage: % of loans with `lmi_flag` among loans with origination LVR above 80 (2dp). One number.",
      "SELECT ROUND(100.0*COUNT(*) FILTER (WHERE lmi_flag)/COUNT(*),2) FROM loan WHERE lvr_at_origination_pct>80"),
    P(2, "Current LVR distribution from the ECL table at 2025-12-31: count and balance (EAD, 0dp) in bands `<=60`, `60-80`, `80-90`, `>90` (upper inclusive). `band`, `loans`, `ead`; sorted by band lower bound.",
      "SELECT b, COUNT(*), ROUND(SUM(ead),0) FROM (SELECT ead, CASE WHEN current_lvr_pct<=60 THEN '<=60' WHEN current_lvr_pct<=80 THEN '60-80' WHEN current_lvr_pct<=90 THEN '80-90' ELSE '>90' END AS b, CASE WHEN current_lvr_pct<=60 THEN 1 WHEN current_lvr_pct<=80 THEN 2 WHEN current_lvr_pct<=90 THEN 3 ELSE 4 END AS k FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31') GROUP BY b, k ORDER BY k"),
    P(2, "Latest non-zero AVM per property: how many properties have a latest AVM (`valuation_type` 'Automated Valuation (AVM)', amount > 0, date <= 2025-12-31)? One number.",
      "SELECT COUNT(DISTINCT property_id) FROM property_valuation WHERE valuation_type='Automated Valuation (AVM)' AND valuation_amount>0 AND valuation_date<=DATE '2025-12-31'"),
    P(2, "Cross-collateral: loans with more than one security and their number of securities, with total `allocated_value` (0dp). Show the 10 largest by total allocated value. `loan_id`, `securities`, `total_allocated`; sorted by total descending then id.",
      "SELECT loan_id, COUNT(*), ROUND(SUM(allocated_value),0) AS t FROM loan_security GROUP BY 1 HAVING COUNT(*)>1 ORDER BY t DESC, 1 LIMIT 10"),
    P(2, "Does the stored security value tie back? For loans, compare `security_value_at_origination` with the sum of `allocated_value` across `loan_security`: count loans where they differ by more than $1. One number.",
      "SELECT COUNT(*) FROM loan l JOIN (SELECT loan_id, SUM(allocated_value) AS v FROM loan_security GROUP BY 1) s USING (loan_id) WHERE ABS(l.security_value_at_origination - s.v) > 1"),
    P(3, "Indexed current LVR: for live loans at 2025-12-31 estimate property value now = `security_value_at_origination` * (HPI of the property's state at 2025-12-31 / HPI at the origination month-end). Then current LVR = balance / value. Return the % of live loans with indexed LVR above 80 (2dp) and above 100 (2dp). `pct_gt80`, `pct_gt100`.",
      """WITH x AS (SELECT s.closing_balance / (l.security_value_at_origination * n.price_index / o.price_index) * 100 AS clvr
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode
 JOIN ref_property_price_index o ON o.state=d.state AND o.month_end_date=last_day(l.origination_date) JOIN ref_property_price_index n ON n.state=d.state AND n.month_end_date=DATE '2025-12-31'
 WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed')
SELECT ROUND(100.0*COUNT(*) FILTER (WHERE clvr>80)/COUNT(*),2), ROUND(100.0*COUNT(*) FILTER (WHERE clvr>100)/COUNT(*),2) FROM x"""),
    P(3, "Price fall scenario: a 20% fall in property values. Using `ecl_provision_quarterly` at 2025-12-31 (`ead`, `current_lvr_pct`), the number of loans and EAD (0dp) where the stressed LVR (`current_lvr_pct / 0.8`) exceeds 100. `loans`, `ead`.",
      "SELECT COUNT(*), ROUND(SUM(ead),0) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND current_lvr_pct/0.8>100"),
    P(3, "AVM zero problem: how many live loans (at 2025-12-31) have a property whose most recent valuation row (by date, valuation_id) is an AVM with amount 0? These would break an LVR calculation. One number.",
      "SELECT COUNT(*) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN (SELECT property_id, valuation_type, valuation_amount FROM property_valuation WHERE valuation_date<=DATE '2025-12-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY property_id ORDER BY valuation_date DESC, valuation_id DESC)=1) v ON v.property_id=l.property_id WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND v.valuation_type='Automated Valuation (AVM)' AND v.valuation_amount=0"),
    P(3, "Valuation shift between origination and now for the same property (latest non-zero AVM vs `security_value_at_origination`): the average % change (1dp) per property state, for loans with such an AVM. `state`, `avg_change_pct`; sorted by state.",
      "SELECT d.state, ROUND(AVG(100*(v.valuation_amount/l.security_value_at_origination-1)),1) FROM loan l JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode JOIN (SELECT property_id, valuation_amount FROM property_valuation WHERE valuation_type='Automated Valuation (AVM)' AND valuation_amount>0 AND valuation_date<=DATE '2025-12-31' QUALIFY ROW_NUMBER() OVER (PARTITION BY property_id ORDER BY valuation_date DESC, valuation_id DESC)=1) v ON v.property_id=l.property_id WHERE l.purpose<>'Internal Refinance' GROUP BY 1 ORDER BY 1"),
    P(3, "Negative equity watch: loans in the ECL table at 2025-12-31 with `current_lvr_pct > 100`, by stage. `ifrs9_stage`, `loans`, `ead` (0dp); sorted by stage.",
      "SELECT ifrs9_stage, COUNT(*), ROUND(SUM(ead),0) FROM ecl_provision_quarterly WHERE reporting_date=DATE '2025-12-31' AND current_lvr_pct>100 GROUP BY 1 ORDER BY 1", empty_ok=True),
])
