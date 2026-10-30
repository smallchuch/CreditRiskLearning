#!/usr/bin/env python3
"""
Pandas Grind 4 Lyfe - answer checker.

    python grade.py                     grade every answer file you have written
    python grade.py 06                  grade a whole concept (prefix match: 06, 06_group, groupby ...)
    python grade.py 06 q03              grade one question
    python grade.py 06 q03 --expected   show the first rows of the expected result (not the code)
    python grade.py 06 q03 --solution   print the reference solution (logged as 'peeked')
    python grade.py --next              show the next question you have not passed (add a concept: --next 06)
    python grade.py --random            a random unpassed question (add a concept to narrow it)
    python grade.py --status            progress table only
    python grade.py --review            rebuild progress/REVIEW_ME.md (your code + status, for Claude to review)

Your answers live in  answers/<concept>/qNN.py  - write your code under the header and put the answer
in a variable called `result`. Each file is run fresh, on its own, so it must do everything it needs
(no leftovers from another cell or file).

How results are compared
  * `result` can be a DataFrame, a Series, a list, a dict or a single value.
  * A meaningful index (group keys, labels) counts as leading columns. A plain 0, 1, 2 ... index
    (or the leftover integer index after filtering) is ignored.
  * Column ORDER matters, names don't. Row order only matters when the question says "sorted".
  * Numbers match within a small tolerance (see the question). NaN / None / NaT all count as missing.
"""
import argparse
import contextlib
import csv
import datetime
import decimal
import hashlib
import io
import json
import math
import os
import sys
import time
import traceback

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.environ.setdefault("MPLBACKEND", "Agg")      # plt.show() must never block the grader

META_PATH = os.path.join(ROOT, "_grader", "problems.json")
LOG = os.path.join(ROOT, "progress", "attempts.csv")
STAR = {1: "*", 2: "**", 3: "***"}


# ----------------------------------------------------------------------------------------------
# Turning any answer into rows of plain Python values
# ----------------------------------------------------------------------------------------------
def norm(v):
    """One cell -> None / int / float / str."""
    import numpy as np
    import pandas as pd
    if v is None:
        return None
    if isinstance(v, (float, np.floating)):
        return None if math.isnan(v) else float(v)
    if isinstance(v, (bool, np.bool_)):
        return int(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, decimal.Decimal):
        return float(v)
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(v, (pd.Timestamp, datetime.datetime)):
        if (v.hour, v.minute, v.second, v.microsecond) == (0, 0, 0, 0):
            return v.strftime("%Y-%m-%d")
        return v.isoformat()
    if isinstance(v, datetime.date):
        return v.isoformat()
    if isinstance(v, pd.Timedelta):
        return float(v.days) if v.seconds == 0 and v.microseconds == 0 else v.total_seconds() / 86400
    return str(v)


def _plain_index(idx):
    """True when the index carries no information (unnamed integers)."""
    import pandas as pd
    if isinstance(idx, pd.MultiIndex):
        return False
    if idx.name is not None:
        return False
    return pd.api.types.is_integer_dtype(idx.dtype)


def to_frame(result, keep_index=None):
    """Any answer -> DataFrame with a default index.
    keep_index: None = decide automatically, True / False = force (used for a lenient second try)."""
    import numpy as np
    import pandas as pd
    if isinstance(result, pd.Series):
        df = result.to_frame()
    elif isinstance(result, pd.DataFrame):
        df = result
    elif isinstance(result, dict):
        df = pd.DataFrame({"key": list(result.keys()), "value": list(result.values())})
        keep_index = False if keep_index is None else keep_index
    elif isinstance(result, np.ndarray):
        df = pd.DataFrame(result if result.ndim > 1 else {"value": result})
    elif isinstance(result, (list, tuple, set)):
        items = list(result)
        if items and all(isinstance(x, (list, tuple)) for x in items):
            df = pd.DataFrame([list(x) for x in items])
        else:
            df = pd.DataFrame({"value": items})
    elif isinstance(result, pd.Index):
        df = pd.DataFrame({"value": list(result)})
    else:
        df = pd.DataFrame({"value": [result]})
    if keep_index is None:
        keep_index = not _plain_index(df.index)
    df = df.reset_index() if keep_index else df.reset_index(drop=True)
    return df


def to_rows(result, keep_index=None):
    df = to_frame(result, keep_index)
    cols = [str(c) for c in df.columns]
    rows = [tuple(norm(v) for v in r) for r in df.itertuples(index=False, name=None)]
    return cols, rows


def keyof(row):
    out = []
    for v in row:
        if v is None:
            out.append((0, 0.0, ""))
        elif isinstance(v, (int, float)):
            out.append((1, round(float(v), 2), ""))
        else:
            out.append((2, 0.0, str(v)))
    return tuple(out)


def same(a, b, tol):
    if a is None or b is None:
        return a is None and b is None
    num = (int, float)
    if isinstance(a, num) and isinstance(b, num):
        return abs(a - b) <= max(tol, 1e-9 * max(abs(a), abs(b)))
    return str(a) == str(b)


def compare_rows(s, e, ecols, order, tol):
    if len(s[0]) != len(ecols):
        return False, f"column count: you returned {len(s[0])} ({', '.join(s[0])}), expected {len(ecols)} ({', '.join(ecols)})"
    srows, erows = list(s[1]), [tuple(r) for r in e]
    if len(srows) != len(erows):
        return False, f"row count: you returned {len(srows):,}, expected {len(erows):,}"
    if not order:
        srows.sort(key=keyof)
        erows.sort(key=keyof)
    for i, (a, b) in enumerate(zip(srows, erows)):
        if not all(same(x, y, tol) for x, y in zip(a, b)):
            note = "" if order else "\n        (rows compared after sorting both sides)"
            return False, f"first difference at row {i + 1}:\n        yours    = {a}\n        expected = {b}{note}"
    return True, ""


def compare(result, expected, order, tol):
    """Try the natural reading of `result` first; if the shape is off, try the other index choice."""
    ecols, erows = expected["cols"], expected["rows"]
    first = to_rows(result)
    ok, why = compare_rows(first, erows, ecols, order, tol)
    if ok or not why.startswith("column count"):
        return ok, why
    import pandas as pd
    if isinstance(result, (pd.Series, pd.DataFrame)):
        for keep in (True, False):
            alt = to_rows(result, keep_index=keep)
            if len(alt[0]) == len(ecols):
                ok2, why2 = compare_rows(alt, erows, ecols, order, tol)
                if ok2:
                    return True, ""
                return False, why2 + ("\n        (compared " + ("with" if keep else "without") + " your index as a column)")
    if len(first[0]) == len(ecols) - 1:
        why += "\n        hint: is one of the expected columns sitting in your index? (.reset_index())"
    elif len(first[0]) == len(ecols) + 1:
        why += "\n        hint: an extra column - maybe the index came along (.reset_index(drop=True)) or one column too many"
    return False, why


# ----------------------------------------------------------------------------------------------
# Running an answer file
def answer_body(code):
    """The part of the file under the last '# %%' cell marker (the marker line itself excluded)."""
    if "# %%" not in code:
        return code.strip()
    tail = code.rsplit("# %%", 1)[1]
    return tail.split("\n", 1)[1].strip() if "\n" in tail else ""


# ----------------------------------------------------------------------------------------------
def run_answer(path):
    """Run one answer file in a fresh namespace. Returns (status, result_or_message, seconds)."""
    code = _text(path)
    body = answer_body(code)
    if body in ("", "result = None"):          # untouched stub: don't bother running it
        return "EMPTY", None, 0.0
    ns = {"__file__": os.path.abspath(path), "__name__": "__graded__"}
    out = io.StringIO()
    t0 = time.time()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(code, path, "exec"), ns)
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        line = next((f.lineno for f in reversed(tb) if os.path.abspath(f.filename) == os.path.abspath(path)), None)
        where = f" (line {line})" if line else ""
        return "ERROR", f"{type(e).__name__}{where}: {str(e).splitlines()[0][:300] if str(e) else ''}", time.time() - t0
    finally:
        try:
            import matplotlib.pyplot as plt
            plt.close("all")
        except Exception:
            pass
    secs = time.time() - t0
    if "result" not in ns:
        return "ERROR", "no variable called `result` - put your final answer in result = ...", secs
    if ns["result"] is None:
        return "EMPTY", None, secs
    return "OK", ns["result"], secs


# ----------------------------------------------------------------------------------------------
# Progress, selection, commands
# ----------------------------------------------------------------------------------------------
def _text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_meta():
    return json.loads(_text(META_PATH))


def expected_of(qid):
    p = os.path.join(ROOT, "_grader", "expected", qid.replace("/", "__") + ".json")
    return json.loads(_text(p))


def attempts():
    d = {}
    if os.path.exists(LOG):
        with open(LOG, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                d.setdefault(row["qid"], []).append(row)
    return d


def log(qid, status, secs, text):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    new = not os.path.exists(LOG)
    with open(LOG, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp", "qid", "status", "seconds", "code_hash"])
        w.writerow([datetime.datetime.now().isoformat(timespec="seconds"), qid, status, f"{secs:.2f}",
                    hashlib.md5(text.encode()).hexdigest()[:8]])


def select(meta, concept, q):
    ids = [m["qid"] for m in meta["problems"]]
    if concept:
        c = concept.lower()

        def hit(i):
            key = i.lower().split("/")[0]
            code = key.split("_")[0]
            return c == code or key.startswith(c) or (not c.isdigit() and len(c) > 3 and c in key)
        ids = [i for i in ids if hit(i)]
    if q:
        q = q.lower().lstrip("q")
        want = (f"q{q}", f"q{int(q):02d}") if q.isdigit() else (q,)
        ids = [i for i in ids if i.lower().split("/")[1] in want]
    return ids


def status_table(meta):
    att = attempts()
    by = {}
    for m in meta["problems"]:
        c = m["qid"].split("/")[0]
        a = att.get(m["qid"], [])
        s = by.setdefault(c, [0, 0, 0])
        s[0] += 1
        s[1] += any(r["status"] == "PASS" for r in a)
        s[2] += bool(a)
    print("\n  concept                                  solved / total   attempted")
    print("  " + "-" * 66)
    tot = [0, 0]
    for c, (n, s, a) in by.items():
        bar = "#" * int(20 * s / n) + "." * (20 - int(20 * s / n))
        print(f"  {c:<38} {s:>4} / {n:<4} {bar}  {a}")
        tot[0] += n
        tot[1] += s
    print("  " + "-" * 66)
    print(f"  TOTAL                                  {tot[1]:>4} / {tot[0]:<4}   ({100 * tot[1] / max(tot[0], 1):.0f}%)")


def build_review(meta):
    att = attempts()
    out = ["# Review queue\n", "Point Claude at this file: every attempted answer with its latest status.\n"]
    for m in meta["problems"]:
        qid = m["qid"]
        p = os.path.join(ROOT, "answers", qid + ".py")
        if qid not in att or not os.path.exists(p):
            continue
        last = att[qid][-1]
        body = answer_body(_text(p))
        out.append(f"\n## {qid} - {last['status']} ({len(att[qid])} attempt(s))\n")
        out.append("**Question:** " + m["text"].replace("\n", " ")[:700] + "\n")
        out.append("```python\n" + body + "\n```\n")
    path = os.path.join(ROOT, "progress", "REVIEW_ME.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("wrote progress/REVIEW_ME.md")


def pick(meta, concept, rand):
    import random
    import textwrap
    att = attempts()
    ids = select(meta, concept, None)
    todo = [i for i in ids if not any(a["status"] == "PASS" for a in att.get(i, []))]
    if not todo:
        return print("Nothing left in that selection - everything is passed. Nice.")
    qid = random.choice(todo) if rand else todo[0]
    m = {x["qid"]: x for x in meta["problems"]}[qid]
    print(f"\n  {qid}   {STAR[m['level']]}   ({len(todo)} left in this selection)\n")
    for line in m["text"].splitlines():
        print("  " + "\n  ".join(textwrap.wrap(line, 96) or [""]))
    print(f"\n  Return {len(m['cols'])} column(s), in the order the question gives them.")
    print(f"\n  Write your answer in:  answers/{qid}.py\n  Then check it with:     grade {qid.split('/')[0].split('_')[0]} {qid.split('/')[1]}\n")


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("concept", nargs="?")
    ap.add_argument("q", nargs="?")
    for flag in ("expected", "solution", "status", "review", "next", "random"):
        ap.add_argument("--" + flag, action="store_true")
    args = ap.parse_args()
    meta = load_meta()
    if args.status:
        return status_table(meta)
    if args.review:
        return build_review(meta)
    if args.next or args.random:
        return pick(meta, args.concept, args.random)
    ids = select(meta, args.concept, args.q)
    if not ids:
        sys.exit("no matching questions")
    bymeta = {m["qid"]: m for m in meta["problems"]}
    npass = nfail = nerr = nempty = 0
    for qid in ids:
        m = bymeta[qid]
        path = os.path.join(ROOT, "answers", qid + ".py")
        if args.expected:
            e = expected_of(qid)
            print(f"\n{qid}  expected {len(e['rows']):,} rows x {len(e['cols'])} cols: {e['cols']}")
            for r in e["rows"][:8]:
                print("   ", tuple(r))
            continue
        if args.solution:
            print(f"\n--- reference solution for {qid} ---\n" +
                  _text(os.path.join(ROOT, "_grader", "solutions", qid + ".py")))
            log(qid, "PEEKED", 0, "")
            continue
        if not os.path.exists(path):
            nempty += 1
            continue
        text = _text(path)
        st, res, secs = run_answer(path)
        if st == "EMPTY":
            nempty += 1
            if args.q:
                print(f"  {qid}: nothing written yet (result is still None)")
            continue
        if st == "ERROR":
            nerr += 1
            print(f"  ERROR  {qid}: {res}")
            log(qid, "ERROR", secs, text)
            continue
        try:
            ok, why = compare(res, expected_of(qid), m["order"], m["tol"])
        except Exception as e:
            ok, why = False, f"could not read your result ({type(e).__name__}: {e})"
        slow = f"  (slow: {secs:.1f}s)" if secs > 10 else ""
        if ok:
            npass += 1
            print(f"  PASS   {qid}  {STAR[m['level']]}  {secs:.2f}s{slow}")
            log(qid, "PASS", secs, text)
        else:
            nfail += 1
            print(f"  FAIL   {qid}  {STAR[m['level']]}  {why}")
            log(qid, "FAIL", secs, text)
    if not (args.expected or args.solution):
        print(f"\n  {npass} passed | {nfail} failed | {nerr} errors | {nempty} not attempted")
        if len(ids) > 1:
            status_table(meta)


if __name__ == "__main__":
    main()
