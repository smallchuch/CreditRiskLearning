from . import P

PRIMER = r"""
## Scenario: the RBA moved rates - who is exposed?

Variable loans reprice with the RBA cash rate (with a ~10-day bank lag, see `ref_rba_cash_rate.bank_effective_date`). Fixed loans are protected until `fixed_rate_expiry_date`, then **revert** (the "fixed-rate cliff"). Interest-only loans face a **payment shock** when `io_expiry_date` passes and they convert to P&I.

```
 monthly repayment (P&I):   M = P * r / (1 - (1+r)^-n)        r = annual rate / 12, n = months remaining
 +1% on a $600k, 25-year loan at 6%:  $3,866  ->  $4,228   (+9.4%)   <- the stress test lenders run
```

Your toolkit:
* Snapshot balance + rate give the current exposure.
* `loan_rate_history` gives the rate path of each loan (effective_from/to).
* `loan_event` records reversions ('Fixed rate expired - reverted to variable'), IO conversions and retention discounts.
* Repayment shock = new repayment / old repayment - 1.
"""

CONCEPT = dict(id="cr06_pricing_rate_shock", title="CR06 - Pricing, rate changes and payment shock", primer=PRIMER, problems=[
    P(1, "RBA cash-rate decisions: number of increases and decreases (by `change_bps`) in `ref_rba_cash_rate`. Return `hikes`, `cuts` (ignore the starting row with NULL change).",
      "SELECT COUNT(*) FILTER (WHERE change_bps>0), COUNT(*) FILTER (WHERE change_bps<0) FROM ref_rba_cash_rate"),
    P(1, "Average origination rate (3dp) per origination year for variable loans only. `yr`, `avg_rate`; sorted by year.",
      "SELECT year(origination_date), ROUND(AVG(interest_rate_at_origination_pct),3) FROM loan WHERE rate_type='Variable' GROUP BY 1 ORDER BY 1"),
    P(1, "How many 'Fixed rate expired - reverted to variable' events happened in each calendar year? `yr`, `events`; sorted by year.",
      "SELECT year(event_date), COUNT(*) FROM loan_event WHERE event_type='Fixed rate expired - reverted to variable' GROUP BY 1 ORDER BY 1"),
    P(2, "Pass-through lag: for each RBA decision the `bank_effective_date - decision_date` in days. Return the distinct lag values and count of decisions. `lag_days`, `decisions`; sorted by lag.",
      "SELECT bank_effective_date - decision_date, COUNT(*) FROM ref_rba_cash_rate GROUP BY 1 ORDER BY 1"),
    P(2, "Retention discounts: loans that received a 'Retention discount' rate change - count, and average discount in percentage points (the rate change at that effective date versus the prior row's rate; 2dp). Use LAG on `loan_rate_history` per loan. `loans_discounted`, `avg_cut_pp`. One row (cut positive).",
      "SELECT COUNT(*), ROUND(AVG(prev-interest_rate_pct),2) FROM (SELECT change_reason, interest_rate_pct, LAG(interest_rate_pct) OVER (PARTITION BY loan_id ORDER BY effective_from) AS prev FROM loan_rate_history) WHERE change_reason='Retention discount' AND prev IS NOT NULL"),
    P(2, "Fixed-rate cliff 2026: live loans (snapshot 2025-12-31) with fixed expiry in 2026: count, balance (0dp) and balance-weighted current rate (3dp). `loans`, `balance`, `wtd_rate`.",
      "SELECT COUNT(*), ROUND(SUM(s.closing_balance),0), ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance),3) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.snapshot_date=DATE '2025-12-31' WHERE s.loan_status<>'Closed' AND l.fixed_rate_expiry_date>=DATE '2026-01-01' AND l.fixed_rate_expiry_date<DATE '2027-01-01'"),
    P(2, "Average variable rate on the live book at each of the last 4 year-ends 2022-2025 (balance-weighted, 3dp), rate_type Variable loans (use `loan.rate_type`) and non-closed. `snapshot_date`, `wtd_rate`; sorted by date.",
      "SELECT s.snapshot_date, ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance),3) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.rate_type='Variable' AND s.loan_status<>'Closed' AND s.snapshot_date IN (DATE '2022-12-31', DATE '2023-12-31', DATE '2024-12-31', DATE '2025-12-31') GROUP BY 1 ORDER BY 1"),
    P(3, "Stress test: for live P&I loans at 2025-12-31 compute each loan's current repayment from balance, current rate and remaining term (`term_months - months_on_book`, floor 1), and the repayment at +3pp. Report the total monthly repayment now and stressed (0dp) and % increase (1dp) for loans with remaining term >= 12. `now_total`, `stress_total`, `increase_pct`.",
      """WITH b AS (SELECT s.closing_balance AS p, s.interest_rate_pct/1200 AS r0, (s.interest_rate_pct+3)/1200 AS r1, GREATEST(l.term_months-s.months_on_book,1) AS n
 FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND s.repayment_type='P&I' AND l.term_months-s.months_on_book>=12 AND s.interest_rate_pct>0)
SELECT ROUND(SUM(p*r0/(1-POWER(1+r0,-n))),0), ROUND(SUM(p*r1/(1-POWER(1+r1,-n))),0), ROUND(100*(SUM(p*r1/(1-POWER(1+r1,-n)))/SUM(p*r0/(1-POWER(1+r0,-n)))-1),1) FROM b"""),
    P(3, "IO conversion shock: loans that converted IO -> P&I in 2025 (event 'Interest-only period ended - converted to P&I' in 2025). Average scheduled repayment the month BEFORE and the month AFTER the event month, using the snapshots (the event month's `snapshot_date` = last_day(event_date)). `loans`, `avg_before`, `avg_after`, `increase_pct` (all 1dp except loans). Pairs where both snapshots exist.",
      """WITH e AS (SELECT loan_id, last_day(event_date) AS me FROM loan_event WHERE event_type='Interest-only period ended - converted to P&I' AND event_date>=DATE '2025-01-01' AND event_date<DATE '2026-01-01'),
x AS (SELECT e.loan_id, b.scheduled_repayment AS bef, a.scheduled_repayment AS aft FROM e JOIN loan_monthly_snapshot b ON b.loan_id=e.loan_id AND b.snapshot_date=last_day(e.me - INTERVAL 1 MONTH) JOIN loan_monthly_snapshot a ON a.loan_id=e.loan_id AND a.snapshot_date=last_day(e.me + INTERVAL 1 MONTH))
SELECT COUNT(*), ROUND(AVG(bef),1), ROUND(AVG(aft),1), ROUND(100*(AVG(aft)/AVG(bef)-1),1) FROM x"""),
    P(3, "Customers who got a retention discount and later closed with 'Refinanced to another lender' anyway: count. One number. (Join `loan_event` 'Retention discount applied' to loan closure reason.)",
      "SELECT COUNT(DISTINCT l.loan_id) FROM loan l JOIN loan_event e ON e.loan_id=l.loan_id AND e.event_type='Retention discount applied' WHERE l.closure_reason='Refinanced to another lender'"),
    P(3, "Spread to cash rate: for the live variable book at 2025-12-31, the balance-weighted average margin over the latest RBA cash rate (`cash_rate_pct` of the row with the latest `bank_effective_date <= 2025-12-31`), 2dp. One number: `wtd_margin_pp`.",
      "SELECT ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance) - (SELECT cash_rate_pct FROM ref_rba_cash_rate WHERE bank_effective_date<=DATE '2025-12-31' ORDER BY bank_effective_date DESC LIMIT 1),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE l.rate_type='Variable' AND s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed'"),
    P(3, "Delinquency after a hike: 30+ DPD rate (count, 2dp) at each month-end of 2023 (snapshot dates in 2023) for live loans. `snapshot_date`, `rate_pct`; sorted by date. (Compare it with the hiking cycle in `ref_rba_cash_rate`.)",
      "SELECT snapshot_date, ROUND(100.0*COUNT(*) FILTER (WHERE days_past_due>=30)/COUNT(*),2) FROM loan_monthly_snapshot WHERE snapshot_date>=DATE '2023-01-01' AND snapshot_date<DATE '2024-01-01' AND loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
])
