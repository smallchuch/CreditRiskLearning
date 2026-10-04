#!/usr/bin/env python3
"""
Builds the problem sets from _source/problemsets/*.py :
  * runs every reference solution against bank.duckdb (so nothing ships that does not run)
  * writes expected results (_grader/expected), solutions, problems.json
  * writes PROBLEMS/<concept>.md and creates answer stubs (never overwrites an existing answer file)
Run again any time after the database is rebuilt:   python _source/build_problem_sets.py
"""
import argparse, textwrap, importlib, json, os, pkgutil, re, sys, time
import duckdb

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "_source"))
import problemsets

STAR = {1: "★", 2: "★★", 3: "★★★"}
LEVEL_NAME = {1: "warm-up", 2: "core", 3: "challenge"}


def connect(db):
    con = duckdb.connect()
    con.execute(f"ATTACH '{db}' AS bank (READ_ONLY)"); con.execute("USE bank"); con.execute("ATTACH ':memory:' AS scratch")
    return con


def last_select(con, sql):
    last = None
    for s in con.extract_statements(sql):
        r = con.execute(s)
        if s.type == duckdb.StatementType.SELECT and r.description:
            last = r
            last_rows = r.fetchall(); last_desc = r.description
            last = (last_desc, last_rows)
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(ROOT, "config.json")))
    db = a.db or (cfg["db_path"] if os.path.isabs(cfg["db_path"]) else os.path.normpath(os.path.join(ROOT, cfg["db_path"])))
    con = connect(db)
    mods = sorted(m.name for m in pkgutil.iter_modules(problemsets.__path__))
    meta = []; bad = 0; total_t = time.time()
    for d in ("PROBLEMS", "answers", "_grader/expected", "_grader/solutions"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    mods = [m for m in mods if not m.startswith("_")]
    loaded = {m: importlib.import_module("problemsets." + m) for m in mods}
    extras = {}
    for m in mods:
        if hasattr(loaded[m], "MORE_FOR"):
            extras.setdefault(loaded[m].MORE_FOR, []).extend(loaded[m].PROBLEMS)
    for mn in mods:
        mod = loaded[mn]
        if not hasattr(mod, "CONCEPT"): continue
        if a.only and a.only not in mn: continue
        C = dict(mod.CONCEPT); cid = C["id"]
        C["problems"] = list(C["problems"]) + extras.get(cid, [])
        os.makedirs(os.path.join(ROOT, "answers", cid), exist_ok=True)
        os.makedirs(os.path.join(ROOT, "_grader", "solutions", cid), exist_ok=True)
        md = [f"# {C['title']}", "", f"`answers/{cid}/qNN.sql` &nbsp;|&nbsp; check with: `grade {cid.split('_')[0]}` or `grade {cid.split('_')[0]} q03`", "",
              "Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Return columns **in the order shown**; column names don't matter. "
              "Rows only need to be sorted when the question says so. Numbers match within a small tolerance.", "", C["primer"].strip(), "", "---", "", "## Problems", ""]
        for i, p in enumerate(C["problems"], start=1):
            qn = f"q{i:02d}"; qid = f"{cid}/{qn}"
            t0 = time.time()
            try:
                res = last_select(con, p["sql"])
            except Exception as e:
                print(f"!! {qid} ERROR: {str(e)[:200]}"); bad += 1; continue
            secs = time.time() - t0
            if res is None: print(f"!! {qid} no result"); bad += 1; continue
            desc, rows = res
            if not rows and not p["empty_ok"]: print(f"!! {qid} returns 0 rows"); bad += 1
            if secs > 15: print(f"!! {qid} slow {secs:.1f}s")
            order = p["order"]
            if order is None:
                order = bool(re.search(r"order\s+by[^()]*$", p["sql"].strip().rstrip(";"), re.I | re.S))
            cols = [d[0] for d in desc]
            # expected parquet
            exp = os.path.join(ROOT, "_grader", "expected", f"{cid}__{qn}.parquet").replace("\\", "/")
            con.execute("CREATE OR REPLACE TEMP TABLE _exp AS SELECT * FROM (VALUES (1)) WHERE false")
            # materialise via the same SQL (last select) into a scratch table
            stmts = con.extract_statements(p["sql"])
            for s in stmts[:-1]: con.execute(s)
            con.execute(f"COPY ({stmts[-1].query.rstrip().rstrip(';')}) TO '{exp}' (FORMAT PARQUET)")
            open(os.path.join(ROOT, "_grader", "solutions", cid, qn + ".sql"), "w", encoding="utf-8").write(p["sql"] + "\n")
            meta.append(dict(qid=qid, concept=cid, level=p["level"], order=order, tol=p["tol"], text=p["text"], rows=len(rows), cols=cols))
            sort_note = "Sort the output as described." if order else "Row order does not matter."
            md.append(f"### Q{i:02d} &nbsp; {STAR[p['level']]} &nbsp; ({LEVEL_NAME[p['level']]})")
            md.append("")
            md.append(p["text"])
            md.append("")
            md.append(f"> Return **{len(cols)} column(s)** (in the order the question gives them) &nbsp;|&nbsp; expected **{len(rows):,} row(s)** &nbsp;|&nbsp; {sort_note}")
            if p["hint"]:
                md.append("")
                md.append(f"<details><summary>hint</summary>\n\n{p['hint']}\n\n</details>")
            md.append("")
            stub = os.path.join(ROOT, "answers", cid, qn + ".sql")
            if not os.path.exists(stub):
                body = [f"-- {'=' * 76}", f"-- {cid}  |  Q{i:02d}  |  {STAR[p['level']]} {LEVEL_NAME[p['level']]}", "-- "]
                for line in p["text"].splitlines():
                    for w in (textwrap.wrap(line, 90) or [""]): body.append("-- " + w)
                body += ["-- ", f"-- Return {len(cols)} column(s), in the order the question gives them.", f"-- Expected {len(rows):,} row(s). {sort_note}",
                         f"-- {'=' * 76}", "", "", ""]
                open(stub, "w", encoding="utf-8").write("\n".join(body))
        open(os.path.join(ROOT, "PROBLEMS", cid + ".md"), "w", encoding="utf-8").write("\n".join(md))
        print(f"{cid}: {len(C['problems'])} problems")
    json.dump(dict(built=time.strftime("%Y-%m-%d %H:%M"), problems=meta), open(os.path.join(ROOT, "_grader", "problems.json"), "w"), indent=1)
    print(f"\n{len(meta)} problems built, {bad} problems with issues, {time.time() - total_t:.0f}s")


if __name__ == "__main__":
    main()
