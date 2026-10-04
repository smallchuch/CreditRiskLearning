from . import P

PRIMER = r"""
## Timed drill - interview conditions

The bread-and-butter interview round: join three tables, aggregate, filter groups.

**Rules**
* Set a timer: **40 minutes** for 10 questions (about 4 min each).
* No notes, no looking at the solution. Ctrl-click the data dictionary only if you would be allowed a schema in the interview.
* Say your approach out loud (or write 2 lines of plan as a comment) BEFORE writing SQL: *grain? filters? joins? checks?*
* When time is up, stop. Run `grade dr02` and note your score and which questions ran over.
* Questions get harder as you go; skipping and returning is allowed (and realistic).

Scoring guide: 10/10 = ready | 8+ = solid | below 8 = redo the weak concept sets (the question numbers tell you which).
"""

CONCEPT = dict(id="dr02_joins_aggs_timed", title="DR02 - Timed drill: joins and aggregates", primer=PRIMER, problems=[
    P(1, 'Top 5 branches by total original lending in 2025 (branch name, $0dp). `branch_name`, `amount`; sorted by amount descending.',
      "SELECT b.branch_name, ROUND(SUM(l.original_amount),0) AS a FROM loan l JOIN dim_branch b USING (branch_id) WHERE l.origination_date>=DATE '2025-01-01' AND l.origination_date<DATE '2026-01-01' GROUP BY b.branch_id, b.branch_name ORDER BY a DESC LIMIT 5"),
    P(1, 'Approval rate (decided only, 1dp) by broker tier (A/B/C) using `dim_broker`. `broker_tier`, `approval_pct`; sorted by tier.',
      "SELECT b.broker_tier, ROUND(100.0*COUNT(*) FILTER (WHERE a.decision='Approved')/COUNT(a.decision),1) FROM loan_application a JOIN dim_broker b USING (broker_id) GROUP BY 1 ORDER BY 1"),
    P(2, 'Average bureau score (0dp) of declined vs approved applicants (primary applicant). `decision`, `avg_score`; sorted by decision. Decided applications only.',
      'SELECT a.decision, ROUND(AVG(b.bureau_score),0) FROM loan_application a JOIN credit_bureau_report b ON b.application_id=a.application_id AND b.customer_id=a.primary_customer_id WHERE a.decision IS NOT NULL GROUP BY 1 ORDER BY 1'),
    P(2, 'Assessors who approved more than 1,000 applications: `assessor_staff_id`, `full_name`, `approved`; sorted by approved descending, id.',
      "SELECT a.assessor_staff_id, s.full_name, COUNT(*) AS n FROM loan_application a JOIN dim_staff s ON s.staff_id=a.assessor_staff_id WHERE a.decision='Approved' GROUP BY 1,2 HAVING COUNT(*)>1000 ORDER BY n DESC, 1"),
    P(2, 'Customers with both an investment loan and an owner-occupied purchase loan (as primary): count. One number.',
      "SELECT COUNT(*) FROM (SELECT primary_customer_id FROM loan GROUP BY 1 HAVING COUNT(*) FILTER (WHERE purpose='Purchase - Investment')>0 AND COUNT(*) FILTER (WHERE purpose='Purchase - Owner Occupied')>0)"),
    P(2, 'Total live balance (0dp) by customer `segment` at 2025-12-31 (primary customer). `segment`, `balance`; sorted by segment.',
      "SELECT c.segment, ROUND(SUM(s.closing_balance),0) FROM loan_monthly_snapshot s JOIN loan l USING (loan_id) JOIN customer c ON c.customer_id=l.primary_customer_id WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' GROUP BY 1 ORDER BY 1"),
    P(3, 'Share of loans per `channel` that have a co-borrower (1dp). `channel`, `joint_pct`; sorted by channel.',
      "SELECT l.channel, ROUND(100.0*COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM loan_borrower b WHERE b.loan_id=l.loan_id AND b.borrower_role='Co-applicant'))/COUNT(*),1) FROM loan l GROUP BY 1 ORDER BY 1"),
    P(3, 'Branches whose average loan size in 2025 is above the bank-wide average loan size in 2025. `branch_name`, `avg_amount` (0dp); sorted by avg descending, name.',
      "SELECT b.branch_name, ROUND(AVG(l.original_amount),0) AS a FROM loan l JOIN dim_branch b USING (branch_id) WHERE l.origination_date>=DATE '2025-01-01' GROUP BY b.branch_id, b.branch_name HAVING AVG(l.original_amount) > (SELECT AVG(original_amount) FROM loan WHERE origination_date>=DATE '2025-01-01') ORDER BY a DESC, 1"),
    P(3, 'For each year, the broker with the most loans (ties alphabetical by firm name). `yr`, `firm_name`, `loans`; sorted by year.',
      'SELECT yr, firm_name, n FROM (SELECT year(l.origination_date) AS yr, b.firm_name, COUNT(*) AS n, ROW_NUMBER() OVER (PARTITION BY year(l.origination_date) ORDER BY COUNT(*) DESC, b.firm_name) AS rn FROM loan l JOIN dim_broker b USING (broker_id) GROUP BY 1,2) WHERE rn=1 ORDER BY 1'),
    P(3, 'Customers who applied more than once in the same year and were declined at least once that year. Count distinct customers. One number.',
      "SELECT COUNT(DISTINCT primary_customer_id) FROM (SELECT primary_customer_id FROM loan_application GROUP BY primary_customer_id, year(application_date) HAVING COUNT(*)>1 AND COUNT(*) FILTER (WHERE decision='Declined')>=1)"),
])
