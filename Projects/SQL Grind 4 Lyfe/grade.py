#!/usr/bin/env python3
"""
SQL Grind 4 Lyfe - answer checker.

    python grade.py                 grade every answer file you have written
    python grade.py 05              grade a whole concept (prefix match: 05, 05_agg, joins ...)
    python grade.py 05 q03          grade one question
    python grade.py 05 q03 --expected   show the first rows of the expected result (not the SQL)
    python grade.py 05 q03 --solution   print the reference solution (logged as 'peeked')
    python grade.py --next          show the next question you have not passed (add a concept: --next 05)
    python grade.py --random        a random unpassed question (add a concept to narrow it)
    python grade.py --status        progress table only
    python grade.py --review        rebuild progress/REVIEW_ME.md (queries + results, for Claude to review)

Your answers live in  answers/<concept>/qNN.sql  - write below the comment header, any number of
statements; the LAST statement that returns rows is the one that is graded.
Use  CREATE TEMP ... or the in-memory 'scratch' schema if you need helper tables:
    CREATE TABLE scratch.t AS SELECT ...;
Results are compared with your column ORDER (names don't matter), row order only matters when the
question says "sorted". Numbers match within a small tolerance.
"""
import argparse, csv, datetime, decimal, hashlib, json, os, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
try:
    import duckdb
except ImportError:
    sys.exit("duckdb is not installed. Run:  pip install duckdb")

CFG = json.load(open(os.path.join(ROOT, "config.json")))
DB = CFG["db_path"] if os.path.isabs(CFG["db_path"]) else os.path.normpath(os.path.join(ROOT, CFG["db_path"]))
META = json.load(open(os.path.join(ROOT, "_grader", "problems.json")))
LOG = os.path.join(ROOT, "progress", "attempts.csv")
os.makedirs(os.path.join(ROOT, "progress"), exist_ok=True)
STAR = {1: "*", 2: "**", 3: "***"}


def connect():
    con = duckdb.connect()
    con.execute(f"ATTACH '{DB}' AS bank (READ_ONLY)")
    con.execute("USE bank")
    con.execute("ATTACH ':memory:' AS scratch")
    con.execute("SET threads TO 4")
    return con


def norm(v):
    if v is None: return None
    if isinstance(v, bool): return int(v)
    if isinstance(v, int): return v
    if isinstance(v, (decimal.Decimal, float)): return float(v)
    if isinstance(v, (datetime.datetime, datetime.date)): return v.isoformat()
    return str(v)


def keyof(row):
    return tuple((0, "") if v is None else ((1, round(float(v), 2)) if isinstance(v, (float, int)) else (2, v)) for v in row)


def same(a, b, tol):
    if a is None or b is None: return a is None and b is None
    num = (int, float)
    if isinstance(a, num) and isinstance(b, num):
        return abs(a - b) <= max(tol, 1e-9 * max(abs(a), abs(b)))
    return a == b


def run_sql(con, path):
    text = open(path, encoding="utf-8").read()
    try:
        sts = con.extract_statements(text)
    except Exception as e:
        return "ERROR", str(e).split("\n")[0][:300], None, 0.0
    if not sts: return "EMPTY", None, None, 0.0
    t0 = time.time(); last = None
    try:
        for s in sts:
            r = con.execute(s)
            if s.type == duckdb.StatementType.SELECT and r.description:
                last = (r.description, r.fetchall())
    except Exception as e:
        return "ERROR", str(e).split("\n")[0][:300], None, time.time() - t0
    return "OK", last, None, time.time() - t0


def compare(student, expected, order, tol):
    (sdesc, srows), (edesc, erows) = student, expected
    if len(sdesc) != len(edesc):
        return False, f"column count: you returned {len(sdesc)}, expected {len(edesc)} (expected columns: {', '.join(d[0] for d in edesc)})"
    s = [tuple(norm(v) for v in r) for r in srows]
    e = [tuple(norm(v) for v in r) for r in erows]
    if len(s) != len(e):
        return False, f"row count: you returned {len(s):,}, expected {len(e):,}"
    if not order:
        s.sort(key=keyof); e.sort(key=keyof)
    for i, (a, b) in enumerate(zip(s, e)):
        if not all(same(x, y, tol) for x, y in zip(a, b)):
            return False, f"first difference at row {i + 1}:\n        yours    = {a}\n        expected = {b}" + ("" if order else "\n        (rows compared after sorting both sides)")
    return True, ""


def expected_of(con, qid):
    p = os.path.join(ROOT, "_grader", "expected", qid.replace("/", "__") + ".parquet").replace("\\", "/")
    r = con.execute(f"SELECT * FROM read_parquet('{p}')")
    return r.description, r.fetchall()


def attempts():
    d = {}
    if os.path.exists(LOG):
        for row in csv.DictReader(open(LOG, encoding="utf-8")):
            d.setdefault(row["qid"], []).append(row)
    return d


def log(qid, status, secs, sqltext):
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new: w.writerow(["timestamp", "qid", "status", "seconds", "sql_hash"])
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds"), qid, status, f"{secs:.2f}", hashlib.md5(sqltext.encode()).hexdigest()[:8]])


def select(args):
    ids = [m["qid"] for m in META["problems"]]
    if args.concept:
        c = args.concept.lower()
        def hit(i):
            key = i.lower().split("/")[0]; code = key.split("_")[0]
            return c == code or key.startswith(c) or (not c.isdigit() and len(c) > 3 and c in key)
        ids = [i for i in ids if hit(i)]
    if args.q:
        q = args.q.lower().lstrip("q")
        ids = [i for i in ids if i.lower().split("/")[1] in (f"q{q}", f"q{int(q):02d}" if q.isdigit() else q)]
    return ids


def status_table():
    att = attempts()
    by = {}
    for m in META["problems"]:
        c = m["qid"].split("/")[0]
        a = att.get(m["qid"], [])
        solved = any(r["status"] == "PASS" for r in a)
        s = by.setdefault(c, [0, 0, 0])
        s[0] += 1; s[1] += solved; s[2] += bool(a)
    print("\n  concept                                  solved / total   attempted")
    print("  " + "-" * 66)
    tot = [0, 0, 0]
    for c, (n, s, a) in by.items():
        bar = "#" * int(20 * s / n) + "." * (20 - int(20 * s / n))
        print(f"  {c:<38} {s:>4} / {n:<4} {bar}  {a}")
        tot[0] += n; tot[1] += s; tot[2] += a
    print("  " + "-" * 66)
    print(f"  TOTAL                                  {tot[1]:>4} / {tot[0]:<4}   ({100 * tot[1] / max(tot[0], 1):.0f}%)")


def build_review(con):
    att = attempts(); out = ["# Review queue\n", "Paste/point Claude at this file: it has every attempted answer with its latest status.\n"]
    for m in META["problems"]:
        qid = m["qid"]; p = os.path.join(ROOT, "answers", qid + ".sql")
        if qid not in att or not os.path.exists(p): continue
        last = att[qid][-1]
        out.append(f"\n## {qid} - {last['status']} ({len(att[qid])} attempt(s))\n")
        out.append("**Question:** " + m["text"].replace("\n", " ")[:600] + "\n")
        out.append("```sql\n" + open(p, encoding="utf-8").read().split("-- ====", 2)[-1].strip() + "\n```\n")
    open(os.path.join(ROOT, "progress", "REVIEW_ME.md"), "w", encoding="utf-8").write("\n".join(out))
    print("wrote progress/REVIEW_ME.md")


def pick(args):
    import random
    att = attempts(); ids = select(args)
    todo = [i for i in ids if not any(a["status"] == "PASS" for a in att.get(i, []))]
    if not todo: return print("Nothing left in that selection - everything is passed. Nice.")
    qid = random.choice(todo) if args.random else todo[0]
    m = {x["qid"]: x for x in META["problems"]}[qid]
    path = os.path.join("answers", qid + ".sql")
    print(f"\n  {qid}   {STAR[m['level']]}   ({len(todo)} left in this selection)\n")
    import textwrap
    for line in m["text"].splitlines(): print("  " + "\n  ".join(textwrap.wrap(line, 96) or [""]))
    print(f"\n  Return {len(m['cols'])} column(s), in the order the question gives them.")
    print(f"\n  Write your answer in:  {path}\n  Then check it with:     grade {qid.split('/')[0].split('_')[0]} {qid.split('/')[1]}\n")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("concept", nargs="?"); ap.add_argument("q", nargs="?")
    ap.add_argument("--expected", action="store_true"); ap.add_argument("--solution", action="store_true")
    ap.add_argument("--status", action="store_true"); ap.add_argument("--review", action="store_true")
    ap.add_argument("--all", action="store_true", help="include questions with no answer yet")
    ap.add_argument("--next", action="store_true", help="show the next question you haven't passed yet")
    ap.add_argument("--random", action="store_true", help="show a random question you haven't passed yet")
    args = ap.parse_args()
    if args.status: return status_table()
    if args.next or args.random: return pick(args)
    con = connect()
    if args.review: return build_review(con)
    ids = select(args)
    if not ids: sys.exit("no matching questions")
    meta = {m["qid"]: m for m in META["problems"]}
    npass = nfail = nerr = nempty = 0
    for qid in ids:
        m = meta[qid]; path = os.path.join(ROOT, "answers", qid + ".sql")
        if args.expected:
            d, rows = expected_of(con, qid)
            print(f"\n{qid}  expected {len(rows):,} rows x {len(d)} cols: {[x[0] for x in d]}")
            for r in rows[:8]: print("   ", tuple(norm(v) for v in r))
            continue
        if args.solution:
            print(f"\n--- reference solution for {qid} ---\n" + open(os.path.join(ROOT, "_grader", "solutions", qid + ".sql"), encoding="utf-8").read())
            log(qid, "PEEKED", 0, ""); continue
        if not os.path.exists(path): nempty += 1; continue
        st, res, _, secs = run_sql(con, path)
        sqltext = open(path, encoding="utf-8").read()
        if st == "EMPTY":
            nempty += 1
            if args.q: print(f"  {qid}: nothing written yet")
            continue
        if st == "ERROR":
            nerr += 1; print(f"  ERROR  {qid}: {res}"); log(qid, "ERROR", secs, sqltext); continue
        if res is None:
            nerr += 1; print(f"  ERROR  {qid}: no statement returned rows (did you end with a SELECT?)"); log(qid, "ERROR", secs, sqltext); continue
        ok, why = compare(res, expected_of(con, qid), m["order"], m["tol"])
        slow = f"  (slow: {secs:.1f}s)" if secs > 8 else ""
        if ok:
            npass += 1; print(f"  PASS   {qid}  {STAR[m['level']]}  {secs:.2f}s{slow}"); log(qid, "PASS", secs, sqltext)
        else:
            nfail += 1; print(f"  FAIL   {qid}  {STAR[m['level']]}  {why}"); log(qid, "FAIL", secs, sqltext)
    if not (args.expected or args.solution):
        print(f"\n  {npass} passed | {nfail} failed | {nerr} errors | {nempty} not attempted")
        status_table()


if __name__ == "__main__":
    main()
