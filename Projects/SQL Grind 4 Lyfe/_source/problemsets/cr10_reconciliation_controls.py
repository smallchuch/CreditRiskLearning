from . import P

PRIMER = r"""
## Scenario: audit season - prove the numbers tie

Big 4 advisory / internal audit / model validation all ask the same thing: *"do these two sources agree, and if not, why?"*
This set is a series of **reconciliations and control tests**. Every query returns a count of breaks (ideally 0) or a table of differences.

```
 Source A total   vs   Source B total   ->   difference   ->   which records explain it?
```
Techniques: aggregate both sides to the same grain, `FULL OUTER JOIN` on the key, compare, `COALESCE(a,0) - COALESCE(b,0)`, list the breaks.

Tolerance: money to the cent is rarely exact after rounding - use a threshold (`ABS(diff) > 1`) and say so.
Known quirks are planted in this data; some "breaks" here are real data problems you should be able to explain.
"""

CONCEPT = dict(id="cr10_reconciliation_controls", title="CR10 - Reconciliations and control testing", primer=PRIMER, problems=[
    P(1, "Loan count tie-out: loans on `loan` vs distinct loans in `loan_monthly_snapshot` vs distinct loans in `loan_borrower`. `loan`, `snapshot`, `borrower`.",
      "SELECT (SELECT COUNT(*) FROM loan), (SELECT COUNT(DISTINCT loan_id) FROM loan_monthly_snapshot), (SELECT COUNT(DISTINCT loan_id) FROM loan_borrower)"),
    P(1, "Every loan has exactly one 'Primary' borrower on `loan_borrower`? Count loans with a primary-borrower count different from 1. One number.",
      "SELECT COUNT(*) FROM (SELECT loan_id FROM loan_borrower WHERE borrower_role='Primary' GROUP BY 1 HAVING COUNT(*)<>1) a"),
    P(1, "`loan.primary_customer_id` agrees with the 'Primary' row in `loan_borrower`? Count mismatches. One number.",
      "SELECT COUNT(*) FROM loan l JOIN loan_borrower b ON b.loan_id=l.loan_id AND b.borrower_role='Primary' WHERE b.customer_id<>l.primary_customer_id"),
    P(2, "Origination vs first snapshot: loans where the first snapshot balance (`months_on_book = 0`) differs from `original_amount` by more than $1. Count. One number.",
      "SELECT COUNT(*) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id AND s.months_on_book=0 WHERE ABS(s.closing_balance-l.original_amount)>1"),
    P(2, "Closed-loan control: loans closed on `loan` but still with an 'Active' or 'In Recovery' snapshot AFTER the closed date. Count. One number.",
      "SELECT COUNT(DISTINCT l.loan_id) FROM loan l JOIN loan_monthly_snapshot s ON s.loan_id=l.loan_id WHERE l.closed_date IS NOT NULL AND s.snapshot_date > last_day(l.closed_date) AND s.loan_status<>'Closed'"),
    P(2, "ECL population vs live book: loans in the live book at 2025-12-31 but missing from `ecl_provision_quarterly` at that date, and ECL rows for loans NOT live. `live_not_in_ecl`, `ecl_not_live`.",
      "SELECT (SELECT COUNT(*) FROM loan_monthly_snapshot s WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND NOT EXISTS (SELECT 1 FROM ecl_provision_quarterly e WHERE e.loan_id=s.loan_id AND e.reporting_date=DATE '2025-12-31')), (SELECT COUNT(*) FROM ecl_provision_quarterly e WHERE e.reporting_date=DATE '2025-12-31' AND NOT EXISTS (SELECT 1 FROM loan_monthly_snapshot s WHERE s.loan_id=e.loan_id AND s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed'))"),
    P(2, "EAD vs balance by loan: loans where `ecl_provision_quarterly.ead` at 2025-12-31 differs from the snapshot `closing_balance` by more than $100. Count. One number.",
      "SELECT COUNT(*) FROM ecl_provision_quarterly e JOIN loan_monthly_snapshot s ON s.loan_id=e.loan_id AND s.snapshot_date=e.reporting_date WHERE e.reporting_date=DATE '2025-12-31' AND ABS(e.ead-s.closing_balance)>100"),
    P(3, "Payments vs snapshot: for 2025-12 (payments with `payment_date` in December 2025, status Paid), total paid (0dp) vs total `actual_repayment` in the 2025-12-31 snapshot (0dp) for non-closed loans. `payments`, `snapshot_actual`, `difference`. (Do they reconcile? What might explain a gap?)",
      "SELECT ROUND(p,0), ROUND(s,0), ROUND(p-s,0) FROM (SELECT (SELECT SUM(payment_amount) FROM loan_payment WHERE payment_status='Paid' AND payment_date>=DATE '2025-12-01' AND payment_date<=DATE '2025-12-31') AS p, (SELECT SUM(actual_repayment) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '2025-12-31') AS s)"),
    P(3, "FULL OUTER JOIN reconciliation: loan counts by purpose in `loan` vs count of applications that settled (`current_status='Settled'`) by purpose in `loan_application`. Show `purpose`, `loans`, `settled_apps`, `diff`; sorted by purpose. (Internal refinance loans have no application.)",
      "SELECT COALESCE(a.purpose,b.purpose), COALESCE(a.n,0), COALESCE(b.n,0), COALESCE(a.n,0)-COALESCE(b.n,0) FROM (SELECT purpose, COUNT(*) AS n FROM loan GROUP BY 1) a FULL JOIN (SELECT purpose, COUNT(*) AS n FROM loan_application WHERE current_status='Settled' GROUP BY 1) b ON a.purpose=b.purpose ORDER BY 1"),
    P(3, "Loans to settled applications: settled applications with no loan, and loans with an `application_id` that point to a non-settled application. `settled_no_loan`, `loan_bad_app`. Both expected 0.",
      "SELECT (SELECT COUNT(*) FROM loan_application a WHERE a.current_status='Settled' AND NOT EXISTS (SELECT 1 FROM loan l WHERE l.application_id=a.application_id)), (SELECT COUNT(*) FROM loan l JOIN loan_application a ON a.application_id=l.application_id WHERE a.current_status<>'Settled')"),
    P(3, "Rate history completeness: loans whose current snapshot rate (2025-12-31, non-closed) differs from the `loan_rate_history` row in force at that date by more than 0.01 percentage points (ignore rows keyed as fractions < 1). Count. One number.",
      "SELECT COUNT(*) FROM loan_monthly_snapshot s JOIN loan_rate_history h ON h.loan_id=s.loan_id AND h.effective_from<=s.snapshot_date AND (h.effective_to IS NULL OR h.effective_to>s.snapshot_date) WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND h.interest_rate_pct>=1 AND ABS(h.interest_rate_pct-s.interest_rate_pct)>0.01"),
    P(3, "Hardship flag vs hardship table: snapshots (live) at 2025-12-31 with `hardship_flag` true but no active hardship arrangement covering that date (`start_date <= date <= COALESCE(end_date, 9999)`). Count. One number.",
      "SELECT COUNT(*) FROM loan_monthly_snapshot s WHERE s.snapshot_date=DATE '2025-12-31' AND s.loan_status<>'Closed' AND s.hardship_flag AND NOT EXISTS (SELECT 1 FROM hardship_arrangement h WHERE h.loan_id=s.loan_id AND h.start_date<=s.snapshot_date AND COALESCE(h.end_date,DATE '9999-12-31')>=s.snapshot_date)"),
])
