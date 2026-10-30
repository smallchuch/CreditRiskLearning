#!/usr/bin/env python3
"""
Builds the problem sets from _source/problemsets/*.py :
  * runs every reference solution against the Parquet data (so nothing ships that does not run)
  * writes expected results (_grader/expected), reference solutions (_grader/solutions), problems.json
  * writes PROBLEMS/<concept>.md and creates answer stubs (never overwrites an existing answer file)
Run again any time after the data is rebuilt:   python _source/build_problem_sets.py
    --only 06        rebuild one concept
    --selftest       also run each reference solution through the grader, exactly as an answer would be
"""
import argparse
import importlib
import json
import os
import pkgutil
import re
import sys
import textwrap
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "_source"))
os.environ.setdefault("MPLBACKEND", "Agg")

import problemsets                      # noqa: E402
import grade                            # noqa: E402
from grind import load                  # noqa: E402

STAR = {1: "★", 2: "★★", 3: "★★★"}
LEVEL_NAME = {1: "warm-up", 2: "core", 3: "challenge"}

# variable name used for each table in the stubs and solutions
ALIAS = {
    "loan_monthly_snapshot": "snap",
    "loan_application": "app",
    "application_assessment": "assess",
    "application_applicant": "applicant",
    "credit_bureau_report": "bureau",
}


def var(t):
    return ALIAS.get(t, t)


def reflow(text):
    """Split question text into paragraphs; prose paragraphs are joined into one line, code blocks kept as they are."""
    out, buf, code = [], [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if code:
                buf.append(line)
                out.append("\n".join(buf))
                buf, code = [], False
                continue
            if buf:
                out.append(" ".join(buf))
            buf, code = [line], True
            continue
        if code:
            buf.append(line)
        elif not line.strip():
            if buf:
                out.append(" ".join(buf))
            buf = []
        else:
            buf.append(line.strip())
    if buf:
        out.append("\n".join(buf) if code else " ".join(buf))
    return out


def header(cid, i, p, ncols, nrows, sort_note):
    lines = [f"# {'=' * 92}", f"# {cid}  |  Q{i:02d}  |  {STAR[p['level']]} {LEVEL_NAME[p['level']]}", "#"]
    for para in reflow(p["text"]):
        if para.startswith("```") or "\n" in para:
            lines += ["# " + ln for ln in para.splitlines()]
        else:
            lines += ["# " + w for w in (textwrap.wrap(para, 90) or [""])]
        lines.append("#")
    lines.pop()
    lines += ["#",
              f"# Return {ncols} column(s), in the order the question gives them. Expected {nrows:,} row(s).",
              f"# {sort_note}",
              "# Put your final answer in `result` (DataFrame, Series, list, dict or a single value).",
              f"# {'=' * 92}"]
    return lines


def setup_block(tables):
    lines = ["# %% setup (runs every time - each file must stand on its own)",
             "import os, sys",
             "sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__) if '__file__' in globals() else os.getcwd(), '..', '..')))",
             "import numpy as np",
             "import pandas as pd",
             "from grind import load",
             ""]
    for t in tables:
        lines.append(f"{var(t)} = load('{t}')")
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    mods = sorted(m.name for m in pkgutil.iter_modules(problemsets.__path__) if not m.name.startswith("_"))
    for d in ("PROBLEMS", "answers", "_grader/expected", "_grader/solutions", "progress"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)
    meta_path = os.path.join(ROOT, "_grader", "problems.json")
    old = json.load(open(meta_path)) if (a.only and os.path.exists(meta_path)) else {"problems": []}
    meta, bad, t_all = [], 0, time.time()
    for mn in mods:
        mod = importlib.import_module("problemsets." + mn)
        if not hasattr(mod, "CONCEPT"):
            continue
        C = mod.CONCEPT
        cid = C["id"]
        if a.only and not cid.startswith(a.only):
            meta.extend(m for m in old["problems"] if m["concept"] == cid)
            continue
        os.makedirs(os.path.join(ROOT, "answers", cid), exist_ok=True)
        os.makedirs(os.path.join(ROOT, "_grader", "solutions", cid), exist_ok=True)
        md = [f"# {C['title']}", "",
              f"`answers/{cid}/qNN.py` &nbsp;|&nbsp; check with: `grade {cid.split('_')[0]}` or `grade {cid.split('_')[0]} q03`", "",
              "Levels: ★ warm-up &nbsp; ★★ core &nbsp; ★★★ challenge. Put your answer in `result`. Return columns **in the order shown** "
              "(a meaningful index counts as the leading columns); column names don't matter. Rows only need to be sorted when the "
              "question says so. Numbers match within a small tolerance.", "",
              C["primer"].strip(), "", "---", "", "## Problems", ""]
        for i, p in enumerate(C["problems"], start=1):
            qn = f"q{i:02d}"
            qid = f"{cid}/{qn}"
            ns = {"np": __import__("numpy"), "pd": __import__("pandas"), "load": load}
            for t in p["tables"]:
                ns[var(t)] = load(t)
            t0 = time.time()
            try:
                exec(p["code"], ns)
                cols, rows = grade.to_rows(ns["result"])
            except Exception as e:
                print(f"!! {qid} ERROR: {type(e).__name__}: {str(e)[:300]}")
                bad += 1
                continue
            secs = time.time() - t0
            if not rows and not p["empty_ok"]:
                print(f"!! {qid} returns 0 rows")
                bad += 1
            if len(rows) > 5000:
                print(f"!! {qid} returns {len(rows):,} rows (too many to be a good drill)")
            if secs > 15:
                print(f"!! {qid} slow {secs:.1f}s")
            for named in re.finditer(r"Return ((?:`[^`]+`(?:,\s*|\s*,?\s*then\s+|\s+and\s+)?)+)", p["text"]):
                names = re.findall(r"`([^`]+)`", named.group(1))
                if len(names) == len(cols):
                    cols = names
                    break
            order = p["order"]
            if order is None:
                order = bool(re.search(r"\bsorted\b", p["text"], re.I))
            json.dump({"cols": cols, "rows": rows},
                      open(os.path.join(ROOT, "_grader", "expected", f"{cid}__{qn}.json"), "w", encoding="utf-8"))
            sort_note = "Sort the output as described." if order else "Row order does not matter."
            hdr = header(cid, i, p, len(cols), len(rows), sort_note)
            setup = setup_block(p["tables"])
            sol = hdr + [""] + setup + ["", "# %% your answer", p["code"].strip(), ""]
            open(os.path.join(ROOT, "_grader", "solutions", cid, qn + ".py"), "w", encoding="utf-8").write("\n".join(sol))
            meta.append(dict(qid=qid, concept=cid, level=p["level"], order=order, tol=p["tol"], text=p["text"],
                             rows=len(rows), cols=cols, tables=p["tables"]))
            md.append(f"### Q{i:02d} &nbsp; {STAR[p['level']]} &nbsp; ({LEVEL_NAME[p['level']]})")
            md.append("")
            md.append(p["text"])
            md.append("")
            md.append(f"> Return **{len(cols)} column(s)** (in the order the question gives them) &nbsp;|&nbsp; "
                      f"expected **{len(rows):,} row(s)** &nbsp;|&nbsp; {sort_note} &nbsp;|&nbsp; tables: "
                      + ", ".join(f"`{var(t)}`" for t in p["tables"]))
            if p["hint"]:
                md += ["", f"<details><summary>hint</summary>\n\n{p['hint']}\n\n</details>"]
            md.append("")
            stub = os.path.join(ROOT, "answers", cid, qn + ".py")
            if not os.path.exists(stub):
                body = hdr + [""] + setup + ["", "# %% your answer", "result = None", ""]
                open(stub, "w", encoding="utf-8").write("\n".join(body))
            if a.selftest:
                st, res, _ = grade.run_answer(os.path.join(ROOT, "_grader", "solutions", cid, qn + ".py"))
                ok, why = (False, f"{st}: {res}") if st != "OK" else grade.compare(
                    res, {"cols": cols, "rows": json.load(open(os.path.join(ROOT, "_grader", "expected", f"{cid}__{qn}.json")))["rows"]},
                    order, p["tol"])
                if not ok:
                    print(f"!! {qid} SELFTEST FAIL: {why}")
                    bad += 1
        open(os.path.join(ROOT, "PROBLEMS", cid + ".md"), "w", encoding="utf-8").write("\n".join(md))
        print(f"{cid}: {len(C['problems'])} problems")
    json.dump(dict(built=time.strftime("%Y-%m-%d %H:%M"), problems=meta), open(meta_path, "w", encoding="utf-8"), indent=1)
    print(f"\n{len(meta)} problems built, {bad} problems with issues, {time.time() - t_all:.0f}s")


if __name__ == "__main__":
    main()
