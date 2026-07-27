#!/usr/bin/env python3
"""Rebuild the commit-activity dashboard from live git data.
Run from inside the CreditRiskLearning repo:  python3 build_commit_dashboard.py
Writes commit_activity.html and prints a streak summary.
Counts commits from the user's identities (author email contains 'chuchdeveloper').
"""
import subprocess, json, datetime, collections, os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
AUTHOR = "chuchdeveloper"

def git_dates():
    out = subprocess.run(
        ["git", "log", "--author=" + AUTHOR, "--date=format:%Y-%m-%d", "--pretty=format:%ad"],
        cwd=REPO, capture_output=True, text=True, check=True).stdout
    return sorted([l.strip() for l in out.splitlines() if l.strip()])

def longest_streak(days_set):
    if not days_set: return 0
    ds = sorted(datetime.date.fromisoformat(d) for d in days_set)
    best = run = 1
    for i in range(1, len(ds)):
        run = run + 1 if (ds[i] - ds[i-1]).days == 1 else 1
        best = max(best, run)
    return best

def current_streak(days_set, today):
    d = today
    s = 0
    while d.isoformat() in days_set:
        s += 1; d -= datetime.timedelta(days=1)
    return s

def build():
    dates = git_dates()
    if not dates:
        print("No commits found."); return None
    d = [datetime.date.fromisoformat(x) for x in dates]
    by_day = collections.Counter(dates)
    start, end = min(d), max(d)
    today = datetime.date.today()
    span = (end - start).days + 1
    active = len(set(dates))
    cur = start; daily = []
    while cur <= end:
        daily.append((cur.isoformat(), by_day.get(cur.isoformat(), 0)))
        cur += datetime.timedelta(days=1)
    cum = []; t = 0
    for _, c in daily:
        t += c; cum.append(t)
    by_week = collections.Counter()
    for x in d:
        y, w, _ = x.isocalendar(); by_week[f"{y}-W{w:02d}"] += 1
    dow = collections.Counter(x.strftime("%a") for x in d)
    data = {
        "total": len(dates), "start": start.isoformat(), "end": end.isoformat(),
        "span_days": span, "active_days": active, "pct_active": round(active/span*100, 1),
        "daily": daily, "cumulative": cum, "weekly": sorted(by_week.items()),
        "dow": {k: dow.get(k, 0) for k in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]},
        "monthly": sorted(collections.Counter(x[:7] for x in dates).items()),
        "generated": today.isoformat(),
        "longest_streak": longest_streak(set(dates)),
        "current_streak": current_streak(set(dates), today),
    }
    html = HTML_TEMPLATE.replace("DATA_PLACEHOLDER", json.dumps(data, indent=2))
    with open(os.path.join(REPO, "commit_activity.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return data

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Commit Activity — CreditRiskLearning</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root{--bg:#0d1117;--panel:#161b22;--border:#30363d;--text:#e6edf3;--muted:#8b949e;--accent:#2ea043;--accent2:#58a6ff;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;padding:32px 24px;}
  .wrap{max-width:980px;margin:0 auto}
  h1{font-size:22px;margin:0 0 4px}
  .sub{color:var(--muted);font-size:14px;margin-bottom:24px}
  .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:28px}
  .stat{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:16px}
  .stat .n{font-size:26px;font-weight:700}
  .stat .l{color:var(--muted);font-size:12px;margin-top:4px;text-transform:uppercase;letter-spacing:.04em}
  .card{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:20px}
  .card h2{font-size:15px;margin:0 0 2px}
  .card p{color:var(--muted);font-size:13px;margin:0 0 14px}
  .row{display:grid;grid-template-columns:1.6fr 1fr;gap:20px}
  .chartbox{position:relative;height:300px}
  .chartbox.sm{height:260px}
  @media(max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}.row{grid-template-columns:1fr}}
  .foot{color:var(--muted);font-size:12px;text-align:center;margin-top:8px}
</style>
</head>
<body>
<div class="wrap">
  <h1>Commit Activity</h1>
  <div class="sub" id="sub"></div>
  <div class="stats" id="stats"></div>
  <div class="card">
    <h2>Commits over time</h2>
    <p>Daily commits (bars) and cumulative total (line).</p>
    <div class="chartbox"><canvas id="timeline"></canvas></div>
  </div>
  <div class="row">
    <div class="card">
      <h2>Commits per week</h2>
      <p>ISO week totals.</p>
      <div class="chartbox sm"><canvas id="weekly"></canvas></div>
    </div>
    <div class="card">
      <h2>% of days active</h2>
      <p>Days with &ge;1 commit vs idle days.</p>
      <div class="chartbox sm"><canvas id="active"></canvas></div>
    </div>
  </div>
  <div class="card">
    <h2>Commits by day of week</h2>
    <p>Which weekdays you commit most.</p>
    <div class="chartbox sm"><canvas id="dow"></canvas></div>
  </div>
  <div class="foot" id="foot"></div>
</div>
<script>
const D = DATA_PLACEHOLDER;
const green="#2ea043", blue="#58a6ff", grid="rgba(139,148,158,.15)", muted="#8b949e";
Chart.defaults.color=muted;
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif";
document.getElementById('sub').textContent =
  `Repo: CreditRiskLearning · ${D.total} commits · ${D.start} → ${D.end} · updated ${D.generated}`;
const idle = D.span_days - D.active_days;
const stats=[
  ["Total commits", D.total],
  ["% days active", D.pct_active + "%"],
  ["Current streak", (D.current_streak||0) + "d"],
  ["Longest streak", (D.longest_streak||0) + "d"]
];
document.getElementById('stats').innerHTML = stats.map(s=>
  `<div class="stat"><div class="n">${s[1]}</div><div class="l">${s[0]}</div></div>`).join('');
const labels = D.daily.map(d=>d[0]);
const counts = D.daily.map(d=>d[1]);
new Chart(document.getElementById('timeline'),{
  data:{labels,datasets:[
    {type:'bar',label:'Commits/day',data:counts,backgroundColor:green,borderRadius:2,order:2,yAxisID:'y'},
    {type:'line',label:'Cumulative',data:D.cumulative,borderColor:blue,backgroundColor:blue,tension:.25,pointRadius:0,borderWidth:2,order:1,yAxisID:'y1'}
  ]},
  options:{maintainAspectRatio:false,interaction:{mode:'index',intersect:false},
    scales:{x:{grid:{display:false},ticks:{maxTicksLimit:10,autoSkip:true}},
      y:{beginAtZero:true,position:'left',grid:{color:grid},title:{display:true,text:'per day'}},
      y1:{beginAtZero:true,position:'right',grid:{drawOnChartArea:false},title:{display:true,text:'cumulative'}}},
    plugins:{legend:{labels:{usePointStyle:true}}}}
});
new Chart(document.getElementById('weekly'),{
  type:'bar',
  data:{labels:D.weekly.map(w=>w[0].replace(/^\d+-/,'')),datasets:[{label:'Commits',data:D.weekly.map(w=>w[1]),backgroundColor:green,borderRadius:3}]},
  options:{maintainAspectRatio:false,scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:grid}}},plugins:{legend:{display:false}}}
});
new Chart(document.getElementById('active'),{
  type:'doughnut',
  data:{labels:['Active days','Idle days'],datasets:[{data:[D.active_days,idle],backgroundColor:[green,'#30363d'],borderColor:'#161b22',borderWidth:3}]},
  options:{maintainAspectRatio:false,cutout:'68%',plugins:{legend:{position:'bottom',labels:{usePointStyle:true}},
    tooltip:{callbacks:{label:c=>`${c.label}: ${c.raw} (${(c.raw/D.span_days*100).toFixed(1)}%)`}}}}
});
const dowKeys=Object.keys(D.dow);
new Chart(document.getElementById('dow'),{
  type:'bar',
  data:{labels:dowKeys,datasets:[{label:'Commits',data:dowKeys.map(k=>D.dow[k]),backgroundColor:blue,borderRadius:3}]},
  options:{maintainAspectRatio:false,scales:{x:{grid:{display:false}},y:{beginAtZero:true,grid:{color:grid}}},plugins:{legend:{display:false}}}
});
document.getElementById('foot').textContent =
  `${D.active_days} of ${D.span_days} calendar days had commits (${D.pct_active}%). Includes identities Evan & smallchuch.`;
</script>
</body>
</html>"""

if __name__ == "__main__":
    data = build()
    if data:
        print(json.dumps({k: data[k] for k in
              ["total","active_days","span_days","pct_active","current_streak","longest_streak","end"]}))
