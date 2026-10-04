from . import P

PRIMER = r"""
## Scenario: you've just joined the credit risk analytics team

Your manager says: *"Before anything else, tell me what the book looks like."* This set is the first-week portfolio snapshot every analyst builds.

**Definitions used throughout the credit-risk sets** (write them in your own notes):
* **The live book at 2025-12-31** = rows of `loan_monthly_snapshot` where `snapshot_date = '2025-12-31'` and `loan_status <> 'Closed'`.
* **Exposure / balance** = `closing_balance`.
* **LVR (origination)** = `loan.lvr_at_origination_pct`; current LVR is in `ecl_provision_quarterly.current_lvr_pct`.
* **Concentration** = how much of the book sits in one bucket (state, product, broker, high-LVR...). Regulators and boards watch these.

```
   Live book  -->  slice by:  state | product | purpose | channel | LVR band | repayment type | broker
                   measure:   count | balance | share of total | average rate | weighted LVR
```
Weighted averages: `SUM(x * balance) / SUM(balance)`. Simple averages treat a $50k loan like a $2m loan - committees want the weighted view.
"""

LIVE = "loan_monthly_snapshot s JOIN loan l USING (loan_id)"
CONCEPT = dict(id="cr01_portfolio_concentration", title="CR01 - Portfolio snapshot and concentration", primer=PRIMER, problems=[
    P(1, "Headline numbers: loans in the live book, total balance (0dp) and average balance (0dp). One row: `loans`, `total_balance`, `avg_balance`.",
      "SELECT COUNT(*), ROUND(SUM(closing_balance),0), ROUND(AVG(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'"),
    P(1, "Balance by loan `purpose` with share of book (1dp %). Return `purpose`, `balance` (0dp), `share_pct`; sorted by balance descending.",
      "SELECT l.purpose, ROUND(SUM(s.closing_balance),0) AS b, ROUND(100*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY b DESC"),
    P(1, "Investor vs owner-occupier: using `dim_product.occupancy`, balance (0dp) and share (1dp) by occupancy. Return `occupancy`, `balance`, `share_pct`; sorted by occupancy.",
      "SELECT p.occupancy, ROUND(SUM(s.closing_balance),0), ROUND(100*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN dim_product p ON p.product_id=l.product_id WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Geographic concentration: balance share (1dp) by `dim_postcode.state` of the security property. `state`, `balance` (0dp), `share_pct`; sorted by balance descending.",
      "SELECT d.state, ROUND(SUM(s.closing_balance),0) AS b, ROUND(100*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY b DESC"),
    P(2, "Interest-only share of the live book: % of balance on `repayment_type = 'Interest Only'` at 2025-12-31 (2dp). One number.",
      "SELECT ROUND(100*SUM(closing_balance) FILTER (WHERE repayment_type='Interest Only')/SUM(closing_balance),2) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'"),
    P(2, "Balance-weighted average interest rate (3dp) by `rate_type` of the loan. Return `rate_type`, `wtd_rate`; sorted by `rate_type`. Use snapshot `interest_rate_pct`.",
      "SELECT l.rate_type, ROUND(SUM(s.interest_rate_pct*s.closing_balance)/SUM(s.closing_balance),3) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(2, "Channel mix of the live book by balance (1dp %). `channel`, `share_pct`; sorted by share descending.",
      "SELECT l.channel, ROUND(100*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) AS p FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY p DESC"),
    P(2, "Broker concentration: top 10 brokers by live balance and their share of the whole book (2dp). Return `broker_id`, `balance` (0dp), `share_pct`; sorted by balance descending.",
      "SELECT l.broker_id, ROUND(SUM(s.closing_balance),0) AS b, ROUND(100*SUM(s.closing_balance)/(SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed'),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND l.broker_id IS NOT NULL GROUP BY 1 ORDER BY b DESC, 1 LIMIT 10"),
    P(2, "Large exposures: number of live loans with balance over $1.5m and their combined balance (0dp). Two numbers: `loans`, `balance`.",
      "SELECT COUNT(*), ROUND(SUM(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31' AND loan_status<>'Closed' AND closing_balance>1500000"),
    P(3, "Customer-level concentration: top 10 primary customers by total live balance across all their loans. `primary_customer_id`, `loans`, `total_balance` (0dp); sorted by balance descending, id.",
      "SELECT l.primary_customer_id, COUNT(*), ROUND(SUM(s.closing_balance),0) AS b FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY b DESC, 1 LIMIT 10"),
    P(3, "High-LVR book at origination: share of live balance with `lvr_at_origination_pct > 80` (2dp), and with `> 90` (2dp). Return `pct_gt80`, `pct_gt90`.",
      "SELECT ROUND(100*SUM(s.closing_balance) FILTER (WHERE l.lvr_at_origination_pct>80)/SUM(s.closing_balance),2), ROUND(100*SUM(s.closing_balance) FILTER (WHERE l.lvr_at_origination_pct>90)/SUM(s.closing_balance),2) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed'"),
    P(3, "Product x state: for each property state, the product (`product_name`) with the largest live balance. Return `state`, `product_name`, `balance` (0dp); sorted by state.",
      """SELECT state, product_name, ROUND(b,0) FROM (SELECT d.state, p.product_name, SUM(s.closing_balance) AS b, ROW_NUMBER() OVER (PARTITION BY d.state ORDER BY SUM(s.closing_balance) DESC, p.product_name) AS rn
FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property pr ON pr.property_id=l.property_id JOIN dim_postcode d ON d.postcode=pr.postcode JOIN dim_product p ON p.product_id=l.product_id
WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1,2) WHERE rn=1 ORDER BY 1"""),
    P(3, "Herfindahl-Hirschman index (HHI) of state concentration: sum over states of (share of book)^2 where share is a fraction (e.g. 0.25), times 10,000, rounded to 0dp. One number: `hhi`.",
      "SELECT ROUND(SUM(sh*sh)*10000,0) FROM (SELECT SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER () AS sh FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property p ON p.property_id=l.property_id JOIN dim_postcode d ON d.postcode=p.postcode WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY d.state)"),
    P(3, "Portfolio growth: live balance at each year-end 2019-2025 and the growth vs prior year-end (%, 1dp). Return `year_end` (date), `balance` (0dp), `growth_pct`; sorted by date.",
      """WITH y AS (SELECT snapshot_date, SUM(closing_balance) AS b FROM loan_monthly_snapshot WHERE month(snapshot_date)=12 AND loan_status<>'Closed' GROUP BY 1)
SELECT snapshot_date, ROUND(b,0), ROUND(100*(b/LAG(b) OVER (ORDER BY snapshot_date)-1),1) FROM y ORDER BY 1"""),
    P(3, "Average loan size by origination year for live loans (balance at 2025-12-31 and original amount both, 0dp). Return `yr`, `avg_original`, `avg_balance`; sorted by yr.",
      "SELECT year(l.origination_date), ROUND(AVG(l.original_amount),0), ROUND(AVG(s.closing_balance),0) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
])
