from ._gen import *
MORE_FOR = 'cr01_portfolio_concentration'
PROBLEMS = []
SJ = "FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN property pr ON pr.property_id=l.property_id JOIN dim_postcode d ON d.postcode=pr.postcode"
for s in STATES:
    PROBLEMS.append(P(2, f"Property state `'{s}'` at 2025-12-31: live loans, total balance (0 dp), share of the whole book (2 dp %) and balance-weighted interest rate (3 dp). `loans`, `balance`, `share_pct`, `wtd_rate`.",
      f"SELECT COUNT(*), ROUND(SUM(s.closing_balance),0), ROUND(100*SUM(s.closing_balance)/(SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE {LIVE}),2), ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance),3) {SJ} WHERE {LIVES} AND d.state='{s}'"))
for p in PURPOSES:
    PROBLEMS.append(P(2, f"Purpose `'{p}'` live book at 2025-12-31: loans, balance (0 dp), average origination LVR (1 dp), weighted rate (3 dp). `loans`, `balance`, `avg_lvr`, `wtd_rate`.",
      f"SELECT COUNT(*), ROUND(SUM(s.closing_balance),0), ROUND(AVG(l.lvr_at_origination_pct),1), ROUND(SUM(s.closing_balance*s.interest_rate_pct)/SUM(s.closing_balance),3) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE {LIVES} AND l.purpose='{p}'"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"Channel `'{c}'` live book: balance (0 dp) split by product occupancy. `occupancy`, `balance`, `share_pct` (share within the channel, 1 dp); sorted by occupancy.",
      f"SELECT p.occupancy, ROUND(SUM(s.closing_balance),0), ROUND(100*SUM(s.closing_balance)/SUM(SUM(s.closing_balance)) OVER (),1) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN dim_product p ON p.product_id=l.product_id WHERE {LIVES} AND l.channel='{c}' GROUP BY 1 ORDER BY 1"))
for y in range(2019,2026):
    PROBLEMS.append(P(1, f"Book size at {y}-12-31: live loans, total balance (0 dp), average balance (0 dp), largest balance (0 dp). `loans`, `balance`, `avg_balance`, `max_balance`.",
      f"SELECT COUNT(*), ROUND(SUM(closing_balance),0), ROUND(AVG(closing_balance),0), ROUND(MAX(closing_balance),0) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed'"))
for k in (5,10,20):
    PROBLEMS.append(P(3, f"Top-{k} concentration: the share of the live balance (2 dp %) held by the largest {k} primary customers (by total balance across their loans). One number.",
      f"SELECT ROUND(100*SUM(b)/(SELECT SUM(closing_balance) FROM loan_monthly_snapshot WHERE {LIVE}),2) FROM (SELECT SUM(s.closing_balance) AS b FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) WHERE {LIVES} GROUP BY l.primary_customer_id ORDER BY b DESC LIMIT {k})"))
