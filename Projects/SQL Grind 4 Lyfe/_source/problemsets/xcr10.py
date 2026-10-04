from ._gen import *
MORE_FOR = 'cr10_reconciliation_controls'
PROBLEMS = []
for y in range(2019,2026):
    PROBLEMS.append(P(2, f"Year-end {y}: live loans in the snapshot vs rows in `ecl_provision_quarterly` at {y}-12-31, and the difference. `snapshot_live`, `ecl_rows`, `diff`.",
      f"SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan_monthly_snapshot WHERE snapshot_date=DATE '{y}-12-31' AND loan_status<>'Closed') AS a, (SELECT COUNT(*) FROM ecl_provision_quarterly WHERE reporting_date=DATE '{y}-12-31') AS b)"))
for y in range(2019,2026):
    PROBLEMS.append(P(2, f"Origination tie-out {y}: loans originated in {y} per `loan` vs loans whose first snapshot (`months_on_book = 0`) is in {y}, and the difference. `loans`, `first_snapshots`, `diff`.",
      f"SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE {yr('origination_date',y)}) AS a, (SELECT COUNT(*) FROM loan_monthly_snapshot WHERE months_on_book=0 AND {yr('snapshot_date',y)}) AS b)"))
for y in range(2019,2026):
    PROBLEMS.append(P(3, f"Closure tie-out {y}: loans with `closed_date` in {y} vs loans whose snapshot status first turns 'Closed' in {y} (first `snapshot_date` with `loan_status='Closed'`), and the difference. `closed_loans`, `snapshot_closed`, `diff`.",
      f"SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE {yr('closed_date',y)}) AS a, (SELECT COUNT(*) FROM (SELECT loan_id, MIN(snapshot_date) AS d FROM loan_monthly_snapshot WHERE loan_status='Closed' GROUP BY 1) WHERE {yr('d',y)}) AS b)"))
for c in CHANNELS:
    PROBLEMS.append(P(2, f"`'{c}'` channel: loans on `loan` vs settled applications on `loan_application` for that channel, and the difference (internal refinances have no application). `loans`, `settled_apps`, `diff`.",
      f"SELECT a, b, a-b FROM (SELECT (SELECT COUNT(*) FROM loan WHERE channel='{c}') AS a, (SELECT COUNT(*) FROM loan_application WHERE channel='{c}' AND current_status='Settled') AS b)"))
