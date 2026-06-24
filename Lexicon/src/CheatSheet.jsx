import React, { useState, useMemo, useRef, useEffect } from "react";
import {
  Copy, Check, Download, Upload, Plus, X, Search, Code2, FunctionSquare,
  Trash2, Pencil, ChevronRight, ChevronDown, ArrowLeft, Filter, Save, Loader2,
} from "lucide-react";

// ---------- Seed data ----------
const SEED_FUNCTIONS = [
  { id: "f1", library: "pandas", name: "df.head()", useCases: ["Exploration"], explanation: "Returns the first 5 rows (or n rows) of a DataFrame. First thing you run on any new dataset.", example: "df.head()\ndf.head(10)  # first 10 rows" },
  { id: "f2", library: "pandas", name: "df.info()", useCases: ["Exploration"], explanation: "Prints column dtypes, non-null counts, and memory usage. Use to spot missing data or wrong types fast.", example: "df.info()" },
  { id: "f3", library: "pandas", name: "df.describe()", useCases: ["Exploration", "Statistics"], explanation: "Summary stats (count, mean, std, min, quartiles, max) for numeric columns.", example: "df.describe()\ndf.describe(include='all')  # include categorical too" },
  { id: "f4", library: "pandas", name: "df.shape", useCases: ["Exploration"], explanation: "Returns (rows, columns) as a tuple. No parentheses — it's an attribute, not a method.", example: "rows, cols = df.shape\nprint(df.shape)" },
  { id: "f5", library: "pandas", name: "df.columns", useCases: ["Exploration"], explanation: "Returns the column labels as an Index object. Useful for checking names or looping over columns.", example: "print(df.columns)\nfor col in df.columns:\n    print(col)" },
  { id: "f6", library: "pandas", name: "df.isnull()", useCases: ["Data Cleaning"], explanation: "Returns a same-shaped DataFrame of booleans marking where values are NaN/None.", example: "df.isnull()" },
  { id: "f7", library: "pandas", name: "df.isnull().sum()", useCases: ["Data Cleaning", "Exploration"], explanation: "Counts missing values per column — the standard first check for data quality.", example: "df.isnull().sum()" },
  { id: "f8", library: "pandas", name: "df.fillna()", useCases: ["Data Cleaning"], explanation: "Replaces NaN values with a specified value, method, or per-column mapping.", example: "df.fillna(0)\ndf['col'].fillna(df['col'].mean(), inplace=True)" },
  { id: "f9", library: "pandas", name: "df.dropna()", useCases: ["Data Cleaning"], explanation: "Removes rows (or columns) containing NaN values. Use subset= to target specific columns.", example: "df.dropna()\ndf.dropna(subset=['income'], how='any')" },
  { id: "f10", library: "pandas", name: "df['new'] = ...", useCases: ["Feature Engineering"], explanation: "Creates or overwrites a column by assigning a Series, scalar, or computed expression.", example: "df['debt_to_income'] = df['debt'] / df['income']" },
  { id: "f11", library: "pandas", name: "df.apply()", useCases: ["Feature Engineering"], explanation: "Applies a function along an axis (rows or columns). Slower than vectorised ops but flexible for custom logic.", example: "df['risk_band'] = df['score'].apply(lambda s: 'high' if s < 600 else 'low')" },
  { id: "f12", library: "pandas", name: "df.applymap()", useCases: ["Feature Engineering"], explanation: "Applies a function element-wise to every cell of a DataFrame (not Series-aware). Deprecated in newer pandas in favour of df.map().", example: "df.applymap(lambda x: round(x, 2) if isinstance(x, float) else x)" },
  { id: "f13", library: "pandas", name: "pd.cut()", useCases: ["Feature Engineering", "Binning"], explanation: "Bins continuous values into discrete intervals you define — classic for credit score bands.", example: "df['score_band'] = pd.cut(df['credit_score'], bins=[0,580,670,740,800,850],\n    labels=['Poor','Fair','Good','VeryGood','Excellent'])" },
  { id: "f14", library: "pandas", name: "pd.qcut()", useCases: ["Feature Engineering", "Binning"], explanation: "Bins values into quantile-based buckets (equal-sized groups) rather than fixed-width ranges.", example: "df['income_quartile'] = pd.qcut(df['income'], q=4, labels=['Q1','Q2','Q3','Q4'])" },
  { id: "f15", library: "pandas", name: "pd.to_datetime()", useCases: ["Data Cleaning", "Feature Engineering"], explanation: "Converts a column of strings/numbers into proper datetime objects so you can use .dt accessors.", example: "df['app_date'] = pd.to_datetime(df['app_date'], format='%Y-%m-%d')" },
  { id: "f16", library: "pandas", name: "df['col'].dt.year", useCases: ["Feature Engineering"], explanation: "Extracts the year (or .month, .day, .dayofweek etc.) from a datetime column.", example: "df['app_year'] = df['app_date'].dt.year\ndf['app_month'] = df['app_date'].dt.month" },
  { id: "f17", library: "pandas", name: "df['a'] + df['b']", useCases: ["Feature Engineering"], explanation: "Vectorised element-wise addition between two columns — fast, no loop needed.", example: "df['total_debt'] = df['credit_card_debt'] + df['loan_debt']" },
  { id: "f18", library: "pandas", name: "df['a'] - df['b']", useCases: ["Feature Engineering"], explanation: "Vectorised element-wise subtraction between two columns.", example: "df['net_income'] = df['gross_income'] - df['expenses']" },
  { id: "f19", library: "pandas", name: "df['a'] * df['b']", useCases: ["Feature Engineering"], explanation: "Vectorised element-wise multiplication between two columns.", example: "df['exposure'] = df['loan_amount'] * df['utilisation_rate']" },
  { id: "f20", library: "pandas", name: "df['a'] / df['b']", useCases: ["Feature Engineering"], explanation: "Vectorised element-wise division. Watch for divide-by-zero producing inf/NaN.", example: "df['dti_ratio'] = df['total_debt'] / df['income'].replace(0, np.nan)" },
  { id: "f21", library: "pandas", name: "df.add()", useCases: ["Feature Engineering"], explanation: "Method form of addition, useful because it supports a fill_value for missing data instead of producing NaN.", example: "df['total'] = df['a'].add(df['b'], fill_value=0)" },
  { id: "f22", library: "pandas", name: "df['col']", useCases: ["Selection"], explanation: "Selects a single column as a Series.", example: "scores = df['credit_score']" },
  { id: "f23", library: "pandas", name: "df.loc[]", useCases: ["Selection"], explanation: "Label-based indexing — select rows/columns by index label or boolean mask.", example: "df.loc[df['income'] > 50000, ['name','income']]" },
  { id: "f24", library: "pandas", name: "df.iloc[]", useCases: ["Selection"], explanation: "Position-based indexing — select rows/columns by integer position, like numpy slicing.", example: "df.iloc[0:5, 0:3]  # first 5 rows, first 3 cols" },
  { id: "f25", library: "pandas", name: "df.query()", useCases: ["Selection"], explanation: "Filters rows using a string expression — often more readable than chained boolean masks.", example: "df.query('income > 50000 and default == 0')" },
  { id: "f26", library: "pandas", name: "df.filter()", useCases: ["Selection"], explanation: "Selects columns or rows by label pattern (e.g. regex or substring), not by value.", example: "df.filter(like='score')  # all columns containing 'score'" },
  { id: "f27", library: "pandas", name: "df.groupby()", useCases: ["Aggregation"], explanation: "Splits the DataFrame into groups by key(s) so you can aggregate/transform within each group.", example: "df.groupby('region')['default'].mean()" },
  { id: "f28", library: "pandas", name: "df.agg()", useCases: ["Aggregation"], explanation: "Applies one or more aggregation functions, often after groupby, including different functions per column.", example: "df.groupby('region').agg({'income':'mean', 'default':'sum'})" },
  { id: "f29", library: "pandas", name: "df.transform()", useCases: ["Aggregation", "Feature Engineering"], explanation: "Like agg, but returns a result the same shape as the input — great for group-relative features.", example: "df['income_vs_region_avg'] = df.groupby('region')['income'].transform('mean')" },
  { id: "f30", library: "pandas", name: "pd.merge()", useCases: ["Combining Data"], explanation: "SQL-style join between two DataFrames on key column(s).", example: "pd.merge(loans, customers, on='customer_id', how='left')" },
  { id: "f31", library: "pandas", name: "df.join()", useCases: ["Combining Data"], explanation: "Joins DataFrames primarily on their index rather than a column key.", example: "df.join(other_df, how='left')" },
  { id: "f32", library: "pandas", name: "pd.concat()", useCases: ["Combining Data"], explanation: "Stacks DataFrames together along an axis (rows by default), e.g. combining batches of data.", example: "pd.concat([df_2023, df_2024], axis=0, ignore_index=True)" },
  { id: "f33", library: "pandas", name: "df.pivot_table()", useCases: ["Aggregation", "Combining Data"], explanation: "Reshapes data into a spreadsheet-style pivot with aggregation built in.", example: "df.pivot_table(values='default', index='region', columns='score_band', aggfunc='mean')" },
  { id: "f34", library: "pandas", name: "df.sort_values()", useCases: ["Selection"], explanation: "Sorts rows by one or more column values.", example: "df.sort_values('credit_score', ascending=False)" },
  { id: "f35", library: "pandas", name: "df.sort_index()", useCases: ["Selection"], explanation: "Sorts rows (or columns) by their index labels rather than values.", example: "df.sort_index()" },
  { id: "f36", library: "pandas", name: "df.corr()", useCases: ["Statistics", "Exploration"], explanation: "Computes pairwise correlation between numeric columns — useful for spotting multicollinearity before modelling.", example: "df.corr(numeric_only=True)" },
  { id: "f37", library: "pandas", name: "df.mean()", useCases: ["Statistics"], explanation: "Computes the mean of numeric columns (or a Series).", example: "df['income'].mean()\ndf.mean(numeric_only=True)" },
  { id: "f38", library: "pandas", name: "df.std()", useCases: ["Statistics"], explanation: "Computes the standard deviation of numeric columns (or a Series).", example: "df['income'].std()" },
];

const SEED_SNIPPETS = [
  {
    id: "s1",
    title: "PD bucket via score banding",
    libraries: ["pandas"],
    useCases: ["Feature Engineering", "Binning"],
    description: "Bands a continuous credit score into standard risk tiers for a quick PD proxy view.",
    code:
`bins = [0, 580, 670, 740, 800, 850]
labels = ['Poor', 'Fair', 'Good', 'Very Good', 'Excellent']
df['score_band'] = pd.cut(df['credit_score'], bins=bins, labels=labels)

default_rate_by_band = df.groupby('score_band')['default'].mean()
print(default_rate_by_band)`,
  },
  {
    id: "s2",
    title: "Missing value audit",
    libraries: ["pandas"],
    useCases: ["Data Cleaning", "Exploration"],
    description: "Quick audit of null counts and percentages across all columns, sorted worst first.",
    code:
`null_counts = df.isnull().sum()
null_pct = (null_counts / len(df) * 100).round(2)
audit = pd.DataFrame({'nulls': null_counts, 'pct': null_pct})
audit = audit[audit['nulls'] > 0].sort_values('pct', ascending=False)
print(audit)`,
  },
];

const LIBRARIES = ["pandas", "numpy", "sklearn", "matplotlib", "seaborn", "sql", "python", "other"];

const USE_CASES = [
  "Exploration", "Data Cleaning", "Feature Engineering", "Binning",
  "Selection", "Aggregation", "Combining Data", "Statistics",
  "Modelling", "Evaluation", "Visualization", "Other",
];

const uid = () => Math.random().toString(36).slice(2, 10);

// Back-compat: older exports/autosave files may have snippets with a single `library` string
// rather than a `libraries` array. Normalize on the way in so the rest of the app can assume
// every snippet has a `libraries` array.
function normalizeSnippets(arr) {
  return (Array.isArray(arr) ? arr : []).map((s) =>
    Array.isArray(s.libraries) ? s : { ...s, libraries: s.library ? [s.library] : ["other"] }
  );
}

// ---------- Remember the autosave file handle across reloads (IndexedDB) ----------
// A FileSystemFileHandle is structured-clonable, so it can be stored directly in IndexedDB.
// This is what lets a reload reconnect to the same file instead of forcing Import every time.
const AUTOSAVE_DB = "lexicon-db";
const AUTOSAVE_STORE = "handles";
const AUTOSAVE_KEY = "cheatsheet-autosave-handle";

function idbOpen() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(AUTOSAVE_DB, 1);
    req.onupgradeneeded = () => req.result.createObjectStore(AUTOSAVE_STORE);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
async function idbSet(key, value) {
  const db = await idbOpen();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(AUTOSAVE_STORE, "readwrite");
    tx.objectStore(AUTOSAVE_STORE).put(value, key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}
async function idbGet(key) {
  const db = await idbOpen();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(AUTOSAVE_STORE, "readonly");
    const req = tx.objectStore(AUTOSAVE_STORE).get(key);
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}
async function idbDel(key) {
  const db = await idbOpen();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(AUTOSAVE_STORE, "readwrite");
    tx.objectStore(AUTOSAVE_STORE).delete(key);
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
  });
}

// ---------- VS Code Dark+ syntax colors ----------
const VSC = {
  bg: "#1e1e1e",
  comment: "#6a9955",
  string: "#ce9178",
  number: "#b5cea8",
  keyword: "#569cd6",
  control: "#c586c0",
  func: "#dcdcaa",
  cls: "#4ec9b0",
  variable: "#9cdcfe",
  plain: "#d4d4d4",
};

const PY_CONTROL = new Set([
  "if", "elif", "else", "for", "while", "return", "import", "from", "try",
  "except", "finally", "raise", "with", "yield", "pass", "break", "continue",
  "del", "assert", "async", "await",
]);
const PY_KEYWORD = new Set(["def", "class", "as", "in", "is", "not", "and", "or", "lambda", "global", "nonlocal"]);
const PY_CONST = new Set(["True", "False", "None"]);
const SQL_WORDS = new Set([
  "SELECT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "JOIN", "LEFT", "RIGHT",
  "INNER", "OUTER", "ON", "INSERT", "INTO", "VALUES", "UPDATE", "SET",
  "DELETE", "CREATE", "TABLE", "ALTER", "DROP", "HAVING", "LIMIT",
  "DISTINCT", "UNION", "ALL", "NULL", "IS", "CASE", "WHEN", "THEN", "END",
  "WITH", "AS", "AND", "OR", "NOT", "IN",
]);
const CLASS_WORDS = new Set([
  "DataFrame", "Series", "Index", "Categorical", "LogisticRegression",
  "RandomForestClassifier", "GradientBoostingClassifier", "StandardScaler",
  "MinMaxScaler", "KFold", "StratifiedKFold", "GridSearchCV",
  "RandomizedSearchCV", "Pipeline", "OneHotEncoder", "LabelEncoder",
  "ColumnTransformer", "XGBClassifier", "LGBMClassifier", "CatBoostClassifier",
  "SimpleImputer",
]);

// Single lexer regex: comment | triple-string | string | number | decorator | word | whitespace | fallback-char
const TOKEN_RE =
  /(#[^\n]*)|("""[\s\S]*?"""|'''[\s\S]*?''')|((?:[a-zA-Z]{1,2})?"(?:\\.|[^"\\])*"|(?:[a-zA-Z]{1,2})?'(?:\\.|[^'\\])*')|(\d+\.\d+|\d+)|(@[A-Za-z_]\w*)|([A-Za-z_]\w*)|(\s+)|(.)/g;

function tokenizeCode(code) {
  const out = [];
  let lastNonSpace = "";
  TOKEN_RE.lastIndex = 0;
  let m;
  while ((m = TOKEN_RE.exec(code))) {
    const [, comment, triple, str, num, decorator, word, ws, punct] = m;
    if (comment) {
      out.push({ text: comment, color: VSC.comment, italic: true });
    } else if (triple) {
      out.push({ text: triple, color: VSC.string });
    } else if (str) {
      out.push({ text: str, color: VSC.string });
    } else if (num) {
      out.push({ text: num, color: VSC.number });
    } else if (decorator) {
      out.push({ text: decorator, color: VSC.func });
      lastNonSpace = decorator;
    } else if (word) {
      const upper = word.toUpperCase();
      let color = VSC.plain;
      if (PY_CONTROL.has(word)) color = VSC.control;
      else if (PY_KEYWORD.has(word)) color = VSC.keyword;
      else if (PY_CONST.has(word)) color = VSC.keyword;
      else if (word === "self") color = VSC.variable;
      else if (word === upper && SQL_WORDS.has(upper)) color = VSC.control;
      else if (CLASS_WORDS.has(word)) color = VSC.cls;
      else {
        const rest = code.slice(m.index + word.length);
        const followedByParen = /^\s*\(/.test(rest);
        if (followedByParen) color = VSC.func;
        else if (lastNonSpace === ".") color = VSC.variable;
      }
      out.push({ text: word, color });
      lastNonSpace = word;
    } else if (ws) {
      out.push({ text: ws, color: VSC.plain });
    } else if (punct) {
      out.push({ text: punct, color: VSC.plain });
      lastNonSpace = punct;
    }
  }
  return out;
}

function CodeBlock({ code }) {
  const tokens = useMemo(() => tokenizeCode(code || ""), [code]);
  return (
    <pre
      className="rounded-lg p-3 text-[12.5px] overflow-x-auto whitespace-pre font-mono leading-relaxed border border-black/20"
      style={{ backgroundColor: VSC.bg, color: VSC.plain }}
    >
      <code>
        {tokens.map((tok, i) => (
          <span key={i} style={{ color: tok.color, fontStyle: tok.italic ? "italic" : "normal" }}>
            {tok.text}
          </span>
        ))}
      </code>
    </pre>
  );
}

// ---------- Small UI atoms ----------
function CopyButton({ text, label = "Copy" }) {
  const [copied, setCopied] = useState(false);
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1400);
  };
  return (
    <button
      onClick={handleCopy}
      className={`inline-flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition-colors ${
        copied ? "bg-brandTeal/10 text-brandTealDark" : "bg-slate-100 text-slate-600 hover:bg-slate-200"
      }`}
      title={label}
    >
      {copied ? <Check size={13} /> : <Copy size={13} />}
      {copied ? "Copied" : label}
    </button>
  );
}

function Tag({ children, tone = "slate" }) {
  const tones = {
    slate: "bg-slate-100 text-slate-600",
    emerald: "bg-brandTeal/10 text-brandTealDark",
    amber: "bg-brandOrange/10 text-brandOrange",
  };
  return (
    <span className={`inline-block rounded-full px-2 py-0.5 text-[11px] font-medium ${tones[tone]}`}>
      {children}
    </span>
  );
}

function MultiTagPicker({ selected, onToggle, options = USE_CASES }) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {options.map((uc) => {
        const active = selected.includes(uc);
        return (
          <button
            key={uc}
            type="button"
            onClick={() => onToggle(uc)}
            className={`rounded-full border px-2.5 py-1 text-xs font-medium transition-colors ${
              active
                ? "border-brandTeal bg-brandTeal text-white"
                : "border-slate-200 bg-white text-slate-500 hover:border-slate-300"
            }`}
          >
            {uc}
          </button>
        );
      })}
    </div>
  );
}

// ---------- Multi-library picker (for snippets, which can belong to several libraries) ----------
function MultiLibraryPicker({ selected, onToggle, libraries, onAddLibrary }) {
  const [adding, setAdding] = useState(false);
  const [newLib, setNewLib] = useState("");

  const confirmAdd = () => {
    const trimmed = newLib.trim();
    if (trimmed) {
      onAddLibrary(trimmed);
      if (!selected.includes(trimmed)) onToggle(trimmed);
    }
    setNewLib("");
    setAdding(false);
  };

  return (
    <div className="flex flex-wrap gap-1.5 items-center">
      {libraries.map((l) => {
        const active = selected.includes(l);
        return (
          <button
            key={l}
            type="button"
            onClick={() => onToggle(l)}
            className={`rounded-full border px-2.5 py-1 text-xs font-medium transition-colors ${
              active
                ? "border-brandTeal bg-brandTeal text-white"
                : "border-slate-200 bg-white text-slate-500 hover:border-slate-300"
            }`}
          >
            {l}
          </button>
        );
      })}
      {adding ? (
        <span className="inline-flex items-center gap-1">
          <input
            autoFocus
            className="w-28 rounded-md border border-slate-200 px-2 py-1 text-xs"
            placeholder="New library"
            value={newLib}
            onChange={(e) => setNewLib(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") confirmAdd();
              if (e.key === "Escape") { setAdding(false); setNewLib(""); }
            }}
          />
          <button
            type="button"
            onClick={confirmAdd}
            className="rounded-md bg-brandTeal p-1 text-white hover:bg-brandTealDark"
            title="Add library"
          >
            <Check size={12} />
          </button>
          <button
            type="button"
            onClick={() => { setAdding(false); setNewLib(""); }}
            className="rounded-md border border-slate-200 p-1 text-slate-400 hover:text-slate-600"
            title="Cancel"
          >
            <X size={12} />
          </button>
        </span>
      ) : (
        <button
          type="button"
          onClick={() => setAdding(true)}
          className="inline-flex items-center gap-1 rounded-full border border-dashed border-slate-300 px-2.5 py-1 text-xs font-medium text-slate-400 hover:border-brandTeal hover:text-brandTeal"
        >
          <Plus size={11} /> New
        </button>
      )}
    </div>
  );
}

// ---------- Function card ----------
function FunctionCard({ item, onDelete, onEdit }) {
  return (
    <div className="group rounded-xl border border-slate-200 bg-white p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-2 flex-wrap">
          <code className="rounded-md bg-brandNavy px-2 py-1 text-[13px] font-semibold text-brandTeal">
            {item.name}
          </code>
          <Tag tone="emerald">{item.library}</Tag>
        </div>
        <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
          {onEdit && (
            <button
              onClick={() => onEdit(item)}
              className="text-slate-300 hover:text-brandTeal"
              title="Edit"
            >
              <Pencil size={15} />
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(item.id)}
              className="text-slate-300 hover:text-rose-500"
              title="Delete"
            >
              <Trash2 size={15} />
            </button>
          )}
        </div>
      </div>

      <div className="mt-2 flex flex-wrap gap-1.5">
        {item.useCases.map((uc) => (
          <Tag key={uc}>{uc}</Tag>
        ))}
      </div>

      <p className="mt-2.5 text-sm leading-snug text-slate-600">{item.explanation}</p>

      <div className="mt-3 relative">
        <CodeBlock code={item.example} />
        <div className="absolute top-2 right-2">
          <CopyButton text={item.example} />
        </div>
      </div>
    </div>
  );
}

// ---------- Snippet card ----------
function SnippetCard({ item, onDelete, onEdit }) {
  const libs = item.libraries && item.libraries.length ? item.libraries : (item.library ? [item.library] : []);
  return (
    <div className="group rounded-xl border border-slate-200 bg-white p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-brandNavy">{item.title}</h3>
          <div className="mt-1 flex items-center gap-2 flex-wrap">
            {libs.map((l) => (
              <Tag key={l} tone="emerald">{l}</Tag>
            ))}
            {item.useCases.map((uc) => (
              <Tag key={uc}>{uc}</Tag>
            ))}
          </div>
        </div>
        <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
          {onEdit && (
            <button
              onClick={() => onEdit(item)}
              className="text-slate-300 hover:text-brandTeal"
              title="Edit"
            >
              <Pencil size={15} />
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(item.id)}
              className="text-slate-300 hover:text-rose-500"
              title="Delete"
            >
              <Trash2 size={15} />
            </button>
          )}
        </div>
      </div>

      {item.description && (
        <p className="mt-2 text-sm leading-snug text-slate-600">{item.description}</p>
      )}

      <div className="mt-3 relative">
        <CodeBlock code={item.code} />
        <div className="absolute top-2 right-2">
          <CopyButton text={item.code} label="Copy code" />
        </div>
      </div>
    </div>
  );
}

// ---------- Library picker with inline "add new" (single-select, used by functions) ----------
function LibrarySelect({ value, onChange, libraries, onAddLibrary }) {
  const [adding, setAdding] = useState(false);
  const [newLib, setNewLib] = useState("");

  const confirmAdd = () => {
    const trimmed = newLib.trim();
    if (trimmed) {
      onAddLibrary(trimmed);
      onChange(trimmed);
    }
    setNewLib("");
    setAdding(false);
  };

  if (adding) {
    return (
      <div className="flex items-center gap-1">
        <input
          autoFocus
          className="flex-1 rounded-md border border-slate-200 px-3 py-2 text-sm"
          placeholder="New library name"
          value={newLib}
          onChange={(e) => setNewLib(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") confirmAdd();
            if (e.key === "Escape") { setAdding(false); setNewLib(""); }
          }}
        />
        <button
          type="button"
          onClick={confirmAdd}
          className="shrink-0 rounded-md bg-brandTeal p-2 text-white hover:bg-brandTealDark"
          title="Save library"
        >
          <Check size={14} />
        </button>
        <button
          type="button"
          onClick={() => { setAdding(false); setNewLib(""); }}
          className="shrink-0 rounded-md border border-slate-200 p-2 text-slate-400 hover:text-slate-600"
          title="Cancel"
        >
          <X size={14} />
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-1">
      <select
        className="flex-1 rounded-md border border-slate-200 px-3 py-2 text-sm bg-white"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        {libraries.map((l) => (
          <option key={l} value={l}>{l}</option>
        ))}
      </select>
      <button
        type="button"
        onClick={() => setAdding(true)}
        className="shrink-0 rounded-md border border-slate-200 p-2 text-slate-500 hover:border-brandTeal hover:text-brandTeal"
        title="Add new library"
      >
        <Plus size={14} />
      </button>
    </div>
  );
}

// ---------- Add/Edit Function form ----------
function FunctionForm({ mode = "add", initial = null, onSubmit, onClose, libraries, onAddLibrary }) {
  const [name, setName] = useState(initial?.name || "");
  const [library, setLibrary] = useState(initial?.library || "pandas");
  const [useCases, setUseCases] = useState(initial?.useCases || []);
  const [explanation, setExplanation] = useState(initial?.explanation || "");
  const [example, setExample] = useState(initial?.example || "");

  const toggleUseCase = (uc) =>
    setUseCases((prev) => (prev.includes(uc) ? prev.filter((x) => x !== uc) : [...prev, uc]));

  const submit = () => {
    if (!name.trim()) return;
    onSubmit({
      id: mode === "edit" ? initial.id : uid(),
      library,
      name: name.trim(),
      useCases: useCases.length ? useCases : ["Other"],
      explanation: explanation.trim(),
      example: example.trim(),
    });
    onClose();
  };

  return (
    <div className="rounded-xl border border-brandTeal/30 bg-brandTeal/5 p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-brandNavy">{mode === "edit" ? "Edit function" : "Add function"}</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
          <X size={16} />
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <input
          className="rounded-md border border-slate-200 px-3 py-2 text-sm font-mono"
          placeholder="e.g. df.rename()"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <LibrarySelect
          value={library}
          onChange={setLibrary}
          libraries={libraries}
          onAddLibrary={onAddLibrary}
        />
      </div>

      <div>
        <p className="text-xs font-medium text-slate-500 mb-1.5">Use cases (select multiple)</p>
        <MultiTagPicker selected={useCases} onToggle={toggleUseCase} />
      </div>

      <textarea
        className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
        rows={2}
        placeholder="Brief explanation of what it does"
        value={explanation}
        onChange={(e) => setExplanation(e.target.value)}
      />

      <textarea
        className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm font-mono"
        rows={3}
        placeholder="Example code"
        value={example}
        onChange={(e) => setExample(e.target.value)}
      />

      <button
        onClick={submit}
        disabled={!name.trim()}
        className="rounded-md bg-brandTeal px-4 py-2 text-sm font-medium text-white hover:bg-brandTealDark disabled:opacity-40"
      >
        {mode === "edit" ? "Save changes" : "Add to cheat sheet"}
      </button>
    </div>
  );
}

// ---------- Add/Edit Snippet form ----------
function SnippetForm({ mode = "add", initial = null, onSubmit, onClose, libraries, onAddLibrary }) {
  const [title, setTitle] = useState(initial?.title || "");
  const [libs, setLibs] = useState(initial?.libraries || (initial?.library ? [initial.library] : ["pandas"]));
  const [useCases, setUseCases] = useState(initial?.useCases || []);
  const [description, setDescription] = useState(initial?.description || "");
  const [code, setCode] = useState(initial?.code || "");

  const toggleUseCase = (uc) =>
    setUseCases((prev) => (prev.includes(uc) ? prev.filter((x) => x !== uc) : [...prev, uc]));
  const toggleLibrary = (lib) =>
    setLibs((prev) => (prev.includes(lib) ? prev.filter((x) => x !== lib) : [...prev, lib]));

  const submit = () => {
    if (!title.trim() || !code.trim()) return;
    onSubmit({
      id: mode === "edit" ? initial.id : uid(),
      title: title.trim(),
      libraries: libs.length ? libs : ["other"],
      useCases: useCases.length ? useCases : ["Other"],
      description: description.trim(),
      code: code.trim(),
    });
    onClose();
  };

  return (
    <div className="rounded-xl border border-brandTeal/30 bg-brandTeal/5 p-4 space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-brandNavy">{mode === "edit" ? "Edit snippet" : "Add snippet"}</h3>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-600">
          <X size={16} />
        </button>
      </div>

      <input
        className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
        placeholder="Snippet title, e.g. Train/test split with stratify"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <div>
        <p className="text-xs font-medium text-slate-500 mb-1.5">Libraries (select multiple)</p>
        <MultiLibraryPicker selected={libs} onToggle={toggleLibrary} libraries={libraries} onAddLibrary={onAddLibrary} />
      </div>

      <div>
        <p className="text-xs font-medium text-slate-500 mb-1.5">Use cases (select multiple)</p>
        <MultiTagPicker selected={useCases} onToggle={toggleUseCase} />
      </div>

      <textarea
        className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
        rows={2}
        placeholder="Brief description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <textarea
        className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm font-mono"
        rows={6}
        placeholder="Full code snippet"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />

      <button
        onClick={submit}
        disabled={!title.trim() || !code.trim()}
        className="rounded-md bg-brandTeal px-4 py-2 text-sm font-medium text-white hover:bg-brandTealDark disabled:opacity-40"
      >
        {mode === "edit" ? "Save changes" : "Add to cheat sheet"}
      </button>
    </div>
  );
}

// ---------- Sidebar nav tree: Library -> Functions/Snippets -> Use Case -> item ----------
function NavTree({
  tree, expandedLibs, expandedTypes, expandedUCs, focusedItem,
  onSelectLib, onSelectType, onSelectUC, onSelectItem,
}) {
  const libs = Object.keys(tree).sort();
  if (libs.length === 0) {
    return <p className="px-2 text-xs text-slate-400">Nothing to browse yet.</p>;
  }
  return (
    <nav className="space-y-0.5">
      {libs.map((lib) => {
        const node = tree[lib];
        const libOpen = !!expandedLibs[lib];
        const funcCount = Object.values(node.function).reduce((n, arr) => n + arr.length, 0);
        const snipCount = Object.values(node.snippet).reduce((n, arr) => n + arr.length, 0);
        const totalCount = funcCount + snipCount;

        const typeRows = [
          { type: "function", label: "Functions", count: funcCount, Icon: FunctionSquare },
          { type: "snippet", label: "Snippets", count: snipCount, Icon: Code2 },
        ].filter((t) => t.count > 0);

        return (
          <div key={lib}>
            <button
              onClick={() => onSelectLib(lib)}
              className="w-full flex items-center gap-1.5 rounded-md px-2 py-1.5 text-[15px] font-semibold text-brandNavy hover:bg-slate-100"
            >
              {libOpen ? <ChevronDown size={13} /> : <ChevronRight size={13} />}
              <span className="flex-1 text-left truncate">{lib}</span>
              <span className="text-[11px] text-slate-500">{totalCount}</span>
            </button>

            {libOpen && (
              <div className="ml-3 border-l border-slate-100 pl-2 space-y-0.5">
                {typeRows.map(({ type, label, count, Icon }) => {
                  const typeKey = `${lib}::${type}`;
                  const typeOpen = !!expandedTypes[typeKey];
                  const ucMap = node[type];
                  const useCases = Object.keys(ucMap).sort();
                  return (
                    <div key={type}>
                      <button
                        onClick={() => onSelectType(lib, type)}
                        className="w-full flex items-center gap-1.5 rounded-md px-2 py-1 text-sm font-medium text-slate-600 hover:bg-slate-100"
                      >
                        {typeOpen ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
                        <Icon size={12} />
                        <span className="flex-1 text-left truncate">{label}</span>
                        <span className="text-[11px] text-slate-500">{count}</span>
                      </button>

                      {typeOpen && (
                        <div className="ml-3 border-l border-slate-100 pl-2 space-y-0.5">
                          {useCases.map((uc) => {
                            const ucKey = `${lib}::${type}::${uc}`;
                            const ucOpen = !!expandedUCs[ucKey];
                            const items = ucMap[uc];
                            return (
                              <div key={uc}>
                                <button
                                  onClick={() => onSelectUC(lib, type, uc)}
                                  className="w-full flex items-center gap-1.5 rounded-md px-2 py-1 text-[13px] font-medium text-slate-500 hover:bg-slate-100"
                                >
                                  {ucOpen ? <ChevronDown size={11} /> : <ChevronRight size={11} />}
                                  <span className="flex-1 text-left truncate">{uc}</span>
                                  <span className="text-[11px] text-slate-400">{items.length}</span>
                                </button>

                                {ucOpen && (
                                  <div className="ml-3 border-l border-slate-100 pl-2 space-y-0.5">
                                    {items.map((item) => {
                                      const isActive =
                                        focusedItem && focusedItem.id === item.id && focusedItem.type === item._type;
                                      return (
                                        <button
                                          key={item._type + item.id}
                                          onClick={() => onSelectItem(item, lib, uc)}
                                          title={item._label}
                                          className={`w-full flex items-center gap-1.5 rounded-md px-2 py-1 text-[13px] text-left transition-colors ${
                                            isActive ? "bg-brandTeal text-white font-medium" : "text-slate-600 hover:bg-slate-100"
                                          }`}
                                        >
                                          {item._type === "function" ? <FunctionSquare size={11} /> : <Code2 size={11} />}
                                          <span className="truncate font-mono">{item._label}</span>
                                        </button>
                                      );
                                    })}
                                  </div>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </nav>
  );
}

// Google's documented pattern for the File System Access API: a save picker grants readwrite
// implicitly, but the browser can still require it to be re-confirmed before a later write —
// hence "createWritable... not allowed" even on a freshly-picked handle. Check, and only prompt
// (which needs a user gesture) if it isn't already granted.
async function verifyReadWritePermission(handle) {
  const opts = { mode: "readwrite" };
  if ((await handle.queryPermission(opts)) === "granted") return true;
  if ((await handle.requestPermission(opts)) === "granted") return true;
  return false;
}

// ---------- Main App ----------
export default function CreditRiskCheatSheet() {
  const [tab, setTab] = useState("functions");
  const [functions, setFunctions] = useState(SEED_FUNCTIONS);
  const [snippets, setSnippets] = useState(SEED_SNIPPETS);
  const [libraries, setLibraries] = useState(LIBRARIES);

  const [search, setSearch] = useState("");
  const [libraryFilter, setLibraryFilter] = useState("all");
  const [useCaseFilters, setUseCaseFilters] = useState([]);
  const [formMode, setFormMode] = useState(null); // null | 'add' | 'edit'
  const [editingItem, setEditingItem] = useState(null);
  const [importMsg, setImportMsg] = useState("");
  const [filterOpen, setFilterOpen] = useState(false);
  const fileInputRef = useRef(null);
  const filterRef = useRef(null);

  // Autosave-to-file (File System Access API — Chrome/Edge only)
  const autosaveSupported = typeof window !== "undefined" && !!window.showSaveFilePicker;
  const [fileHandle, setFileHandle] = useState(null);
  const [pendingHandle, setPendingHandle] = useState(null); // remembered handle awaiting a permission re-grant
  const [autosaveState, setAutosaveState] = useState("idle"); // idle | saving | saved | error
  const [autosaveError, setAutosaveError] = useState("");
  const writeQueueRef = useRef(Promise.resolve());

  // Reads whatever's already in a handle's file and loads it into state. Shared by the initial
  // connect, the reconnect button, and the silent auto-restore-on-load attempt below.
  const loadFromHandle = async (handle) => {
    let resumed = false;
    try {
      const file = await handle.getFile();
      if (file.size > 0) {
        const text = await file.text();
        const data = JSON.parse(text);
        if (Array.isArray(data.functions)) { setFunctions(data.functions); resumed = true; }
        if (Array.isArray(data.snippets)) { setSnippets(normalizeSnippets(data.snippets)); resumed = true; }
        if (Array.isArray(data.libraries)) setLibraries(data.libraries);
      }
    } catch (readErr) {
      console.warn("Couldn't read existing autosave file contents, starting fresh:", readErr);
    }
    return resumed;
  };

  // On mount, try to pick up the autosave file remembered from last time. If the browser still
  // has the permission grant, this resumes silently with zero clicks. If the grant didn't survive
  // the reload (common after closing the browser, since File System Access permissions aren't
  // guaranteed to persist), fall back to showing a one-click "Reconnect autosave" button instead
  // of forcing a full re-import + re-pick-the-file flow.
  useEffect(() => {
    if (!autosaveSupported) return;
    let cancelled = false;
    (async () => {
      try {
        const handle = await idbGet(AUTOSAVE_KEY);
        if (!handle || cancelled) return;
        const granted = (await handle.queryPermission({ mode: "readwrite" })) === "granted";
        if (cancelled) return;
        if (granted) {
          const resumed = await loadFromHandle(handle);
          if (cancelled) return;
          setFileHandle(handle);
          setImportMsg(resumed ? "Resumed autosave automatically." : "Autosave reconnected.");
          setTimeout(() => setImportMsg(""), 3000);
        } else {
          setPendingHandle(handle);
        }
      } catch (err) {
        console.warn("Couldn't restore remembered autosave file:", err);
      }
    })();
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (!filterOpen) return;
    const handleClick = (e) => {
      if (filterRef.current && !filterRef.current.contains(e.target)) setFilterOpen(false);
    };
    document.addEventListener("mousedown", handleClick);
    return () => document.removeEventListener("mousedown", handleClick);
  }, [filterOpen]);

  // Sidebar nav state
  const [expandedLibs, setExpandedLibs] = useState({});
  const [expandedTypes, setExpandedTypes] = useState({});
  const [expandedUCs, setExpandedUCs] = useState({});
  const [focusedItem, setFocusedItem] = useState(null); // { type, id, library, useCase }

  // Tree shape: { [library]: { function: { [useCase]: items[] }, snippet: { [useCase]: items[] } } }
  const navTree = useMemo(() => {
    const tree = {};
    const ensure = (lib) => {
      if (!tree[lib]) tree[lib] = { function: {}, snippet: {} };
      return tree[lib];
    };
    functions.forEach((f) => {
      const node = ensure(f.library);
      f.useCases.forEach((uc) => {
        if (!node.function[uc]) node.function[uc] = [];
        node.function[uc].push({ ...f, _type: "function", _label: f.name });
      });
    });
    snippets.forEach((s) => {
      const libs = s.libraries && s.libraries.length ? s.libraries : ["other"];
      libs.forEach((lib) => {
        const node = ensure(lib);
        s.useCases.forEach((uc) => {
          if (!node.snippet[uc]) node.snippet[uc] = [];
          node.snippet[uc].push({ ...s, _type: "snippet", _label: s.title });
        });
      });
    });
    return tree;
  }, [functions, snippets]);

  const toggleUseCaseFilter = (uc) =>
    setUseCaseFilters((prev) => (prev.includes(uc) ? prev.filter((x) => x !== uc) : [...prev, uc]));

  const activeList = tab === "functions" ? functions : snippets;

  const librariesInUse = useMemo(() => {
    const set = new Set();
    activeList.forEach((i) => {
      if (tab === "functions") set.add(i.library);
      else (i.libraries || []).forEach((l) => set.add(l));
    });
    return ["all", ...Array.from(set).sort()];
  }, [activeList, tab]);

  const activeFilterCount = (libraryFilter !== "all" ? 1 : 0) + useCaseFilters.length;

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return activeList.filter((item) => {
      const nameField = tab === "functions" ? item.name : item.title;
      const matchesSearch =
        !q ||
        nameField.toLowerCase().includes(q) ||
        (item.explanation || item.description || "").toLowerCase().includes(q) ||
        (item.code || item.example || "").toLowerCase().includes(q);
      const matchesLibrary =
        libraryFilter === "all" ||
        (tab === "functions" ? item.library === libraryFilter : (item.libraries || []).includes(libraryFilter));
      const matchesUseCases =
        useCaseFilters.length === 0 || useCaseFilters.every((uc) => item.useCases.includes(uc));
      return matchesSearch && matchesLibrary && matchesUseCases;
    });
  }, [activeList, search, libraryFilter, useCaseFilters, tab]);

  const closeForm = () => { setFormMode(null); setEditingItem(null); };

  const handleDelete = (id) => {
    if (tab === "functions") setFunctions((prev) => prev.filter((f) => f.id !== id));
    else setSnippets((prev) => prev.filter((s) => s.id !== id));
    setFocusedItem(null);
    if (editingItem?.id === id) closeForm();
  };

  const startEdit = (item) => {
    setFormMode("edit");
    setEditingItem(item);
    setFocusedItem(null);
  };

  // Add or update by id — edit keeps the same id, add generates a fresh one.
  const handleSaveFunction = (item) => {
    setFunctions((prev) => {
      const exists = prev.some((f) => f.id === item.id);
      return exists ? prev.map((f) => (f.id === item.id ? item : f)) : [item, ...prev];
    });
  };
  const handleSaveSnippet = (item) => {
    setSnippets((prev) => {
      const exists = prev.some((s) => s.id === item.id);
      return exists ? prev.map((s) => (s.id === item.id ? item : s)) : [item, ...prev];
    });
  };

  const handleAddLibrary = (name) => {
    setLibraries((prev) => {
      if (prev.includes(name)) return prev;
      const others = prev.filter((l) => l !== "other");
      return [...others, name, "other"];
    });
  };

  const handleExport = () => {
    const payload = { functions, snippets, libraries, exportedAt: new Date().toISOString() };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "credit_risk_cheatsheet.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  // Connect a local file once; every change after that writes straight to it.
  // If the picked file already has data in it (e.g. resuming a past session), load that in first
  // instead of blindly overwriting it with whatever's currently in memory.
  const handleConnectAutosave = async () => {
    if (!autosaveSupported) return;
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: "credit_risk_cheatsheet.json",
        types: [{ description: "JSON", accept: { "application/json": [".json"] } }],
      });

      // Lock in readwrite permission now, while we still have a fresh user gesture to back a
      // prompt if the browser needs one — later automatic writes can't trigger that prompt.
      const ok = await verifyReadWritePermission(handle);
      if (!ok) {
        setImportMsg("Permission to write that file was denied — try Autosave to file again and allow access.");
        setTimeout(() => setImportMsg(""), 5000);
        return;
      }

      const resumed = await loadFromHandle(handle);

      setFileHandle(handle);
      setPendingHandle(null);
      idbSet(AUTOSAVE_KEY, handle).catch((e) =>
        console.warn("Couldn't remember autosave file for next time:", e)
      );
      setImportMsg(resumed ? "Resumed from existing file." : "Autosave connected.");
      setTimeout(() => setImportMsg(""), 3000);
    } catch (err) {
      if (err?.name === "AbortError") return; // user closed the picker — fine
      console.error("Autosave connect failed:", err);
      setImportMsg(`Couldn't enable autosave: ${err?.message || err?.name || "unknown error"}`);
      setTimeout(() => setImportMsg(""), 5000);
    }
  };

  // One click instead of a full re-pick: reuses the remembered handle and just asks the browser
  // to re-grant write permission on it (allowed without a file picker since this runs from a
  // direct button click, i.e. with a user gesture already in hand).
  const reconnectAutosave = async () => {
    if (!pendingHandle) return;
    try {
      const granted = (await pendingHandle.requestPermission({ mode: "readwrite" })) === "granted";
      if (!granted) {
        setImportMsg("Permission denied — use Autosave to file to pick the file again.");
        setTimeout(() => setImportMsg(""), 5000);
        return;
      }
      const resumed = await loadFromHandle(pendingHandle);
      setFileHandle(pendingHandle);
      setPendingHandle(null);
      setImportMsg(resumed ? "Resumed from existing file." : "Autosave reconnected.");
      setTimeout(() => setImportMsg(""), 3000);
    } catch (err) {
      console.error("Autosave reconnect failed:", err);
      setImportMsg(`Couldn't reconnect autosave: ${err?.message || err?.name || "unknown error"}`);
      setTimeout(() => setImportMsg(""), 5000);
    }
  };

  const handleDisconnectAutosave = () => {
    setFileHandle(null);
    setPendingHandle(null);
    setAutosaveState("idle");
    setAutosaveError("");
    idbDel(AUTOSAVE_KEY).catch(() => {});
  };

  // Fires whenever data actually changes (add/delete/edit/import/add-library) — not on every
  // keystroke, since those live in local form state until submitted.
  // Writes are serialized through writeQueueRef so two overlapping calls can never both have a
  // writable stream open on the same file handle at once (a file only allows one at a time — React
  // StrictMode's deliberate double-invoke-effects-on-mount in dev would otherwise trigger exactly
  // that collision and surface as a spurious "Autosave failed" right after connecting).
  useEffect(() => {
    if (!fileHandle) return;
    let cancelled = false;

    writeQueueRef.current = writeQueueRef.current.catch(() => {}).then(async () => {
      if (cancelled) return;
      setAutosaveState("saving");
      try {
        const ok = await verifyReadWritePermission(fileHandle);
        if (!ok) throw new Error("Write permission denied — reconnect via Autosave to file.");
        const payload = { functions, snippets, libraries, exportedAt: new Date().toISOString() };
        const writable = await fileHandle.createWritable();
        await writable.write(JSON.stringify(payload, null, 2));
        await writable.close();
        if (!cancelled) { setAutosaveState("saved"); setAutosaveError(""); }
      } catch (err) {
        console.error("Autosave write failed:", err);
        if (!cancelled) { setAutosaveState("error"); setAutosaveError(err?.message || String(err)); }
      }
    });

    return () => { cancelled = true; };
  }, [functions, snippets, libraries, fileHandle]);

  const handleImportClick = () => fileInputRef.current?.click();

  const handleImportFile = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (evt) => {
      try {
        const data = JSON.parse(evt.target.result);
        const hasFunctions = Array.isArray(data.functions);
        const hasSnippets = Array.isArray(data.snippets);
        if (hasFunctions) setFunctions(data.functions);
        if (hasSnippets) setSnippets(normalizeSnippets(data.snippets));
        if (Array.isArray(data.libraries)) setLibraries(data.libraries);
        if (!hasFunctions && !hasSnippets) {
          setImportMsg(`That JSON doesn't have "functions"/"snippets" arrays at the top level — got keys: ${Object.keys(data).join(", ") || "(none)"}.`);
        } else {
          setImportMsg(`Imported ${data.functions?.length ?? 0} functions, ${data.snippets?.length ?? 0} snippets.`);
        }
      } catch (err) {
        console.error("Import parse failed:", err);
        setImportMsg(`Couldn't read that file — ${err.message}`);
      }
      setTimeout(() => setImportMsg(""), 6000);
    };
    reader.onerror = () => {
      console.error("Import file read failed:", reader.error);
      setImportMsg(`Couldn't read that file — ${reader.error?.message || "file read error"}.`);
      setTimeout(() => setImportMsg(""), 6000);
    };
    reader.readAsText(file);
    e.target.value = "";
  };

  // Sidebar nav handlers
  const selectLib = (lib) => {
    setExpandedLibs((prev) => ({ ...prev, [lib]: !prev[lib] }));
    setLibraryFilter(lib);
    setFocusedItem(null);
  };

  const selectType = (lib, type) => {
    const key = `${lib}::${type}`;
    setExpandedTypes((prev) => ({ ...prev, [key]: !prev[key] }));
    setLibraryFilter(lib);
    setTab(type === "function" ? "functions" : "snippets");
    setFocusedItem(null);
  };

  const selectUC = (lib, type, uc) => {
    const key = `${lib}::${type}::${uc}`;
    setExpandedUCs((prev) => ({ ...prev, [key]: !prev[key] }));
    setLibraryFilter(lib);
    setTab(type === "function" ? "functions" : "snippets");
    setUseCaseFilters([uc]);
    setFocusedItem(null);
  };

  const selectItem = (item, lib, uc) => {
    setTab(item._type === "function" ? "functions" : "snippets");
    setFocusedItem({ type: item._type, id: item.id, library: lib, useCase: uc });
  };

  const clearFocus = () => setFocusedItem(null);

  const focusedFullItem = focusedItem
    ? (focusedItem.type === "function" ? functions : snippets).find((i) => i.id === focusedItem.id)
    : null;

  return (
    <div className="min-h-screen bg-slate-50 font-sans flex">
      {/* Sidebar: Library -> Functions/Snippets -> Use Case -> item nav */}
      <aside className="hidden md:block w-64 shrink-0 border-r border-slate-200 bg-white px-3 py-5 sticky top-0 h-screen overflow-y-auto">
        <h2 className="px-2 text-[13px] font-semibold uppercase tracking-wide text-slate-500 mb-2">Browse</h2>
        <NavTree
          tree={navTree}
          expandedLibs={expandedLibs}
          expandedTypes={expandedTypes}
          expandedUCs={expandedUCs}
          focusedItem={focusedItem}
          onSelectLib={selectLib}
          onSelectType={selectType}
          onSelectUC={selectUC}
          onSelectItem={selectItem}
        />
      </aside>

      <div className="flex-1 min-w-0">
        <div className="mx-auto w-[92%] sm:w-[85%] lg:w-[80%] py-6">
          {/* Header */}
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <h1 className="text-2xl font-bold text-brandNavy tracking-tight">Credit Risk Cheat Sheet</h1>
              <p className="text-sm text-slate-500 mt-0.5">
                Functions &amp; snippets for CreditRiskLearning — export to JSON and keep it in your repo.
              </p>
            </div>
            <div className="flex items-center gap-2">
              {fileHandle ? (
                <div className="flex items-center gap-1.5 text-xs text-slate-500" title={autosaveState === "error" ? autosaveError : undefined}>
                  {autosaveState === "saving" ? (
                    <Loader2 size={13} className="animate-spin text-brandTeal" />
                  ) : autosaveState === "error" ? (
                    <span className="text-rose-500">Autosave failed{autosaveError ? `: ${autosaveError}` : ""}</span>
                  ) : (
                    <Check size={13} className="text-brandTeal" />
                  )}
                  {autosaveState !== "error" && (
                    <span className="truncate max-w-[140px]">
                      {autosaveState === "saving" ? "Saving..." : `Autosaving to ${fileHandle.name}`}
                    </span>
                  )}
                  <button onClick={handleDisconnectAutosave} className="text-slate-400 hover:text-slate-600" title="Stop autosaving">
                    <X size={13} />
                  </button>
                </div>
              ) : pendingHandle ? (
                <button
                  onClick={reconnectAutosave}
                  className="inline-flex items-center gap-1.5 rounded-md border border-brandTeal bg-brandTeal/5 px-3 py-2 text-sm font-medium text-brandTealDark hover:bg-brandTeal/10"
                  title={`Re-grant permission to resume autosaving to ${pendingHandle.name}`}
                >
                  <Save size={14} /> Reconnect autosave
                </button>
              ) : autosaveSupported ? (
                <button
                  onClick={handleConnectAutosave}
                  className="inline-flex items-center gap-1.5 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
                  title="Pick a JSON file to autosave to on every change"
                >
                  <Save size={14} /> Autosave to file
                </button>
              ) : null}
              <input
                ref={fileInputRef}
                type="file"
                accept="application/json"
                className="hidden"
                onChange={handleImportFile}
              />
              <button
                onClick={handleImportClick}
                className="inline-flex items-center gap-1.5 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
              >
                <Upload size={14} /> Import
              </button>
              <button
                onClick={handleExport}
                className="inline-flex items-center gap-1.5 rounded-md bg-brandOrange px-3 py-2 text-sm font-semibold text-brandNavy hover:opacity-90"
              >
                <Download size={14} /> Export JSON
              </button>
            </div>
          </div>

          {!autosaveSupported && (
            <p className="mt-1.5 text-xs text-slate-400">
              Live autosave-to-file needs Chrome or Edge — use Export/Import to carry your data between sessions here.
            </p>
          )}

          {importMsg && (
            <div className="mt-3 rounded-md bg-brandOrange/10 border border-brandOrange/30 px-3 py-2 text-xs text-brandOrange">
              {importMsg}
            </div>
          )}

          {focusedFullItem ? (
            // ---------- Isolated single-item view ----------
            <div className="mt-5">
              <button
                onClick={clearFocus}
                className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-700"
              >
                <ArrowLeft size={14} /> Back to list
              </button>
              <div className="mt-2 text-xs text-slate-400">
                {focusedItem.library} <ChevronRight size={10} className="inline" /> {focusedItem.useCase}
              </div>
              <div className="mt-3">
                {focusedItem.type === "function" ? (
                  <FunctionCard item={focusedFullItem} onDelete={handleDelete} onEdit={startEdit} />
                ) : (
                  <SnippetCard item={focusedFullItem} onDelete={handleDelete} onEdit={startEdit} />
                )}
              </div>
            </div>
          ) : (
            <>
              {/* Tabs */}
              <div className="mt-5 flex gap-1 border-b border-slate-200">
                <button
                  onClick={() => { setTab("functions"); setLibraryFilter("all"); setUseCaseFilters([]); closeForm(); }}
                  className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
                    tab === "functions" ? "border-brandTeal text-brandTeal" : "border-transparent text-slate-400 hover:text-slate-600"
                  }`}
                >
                  <FunctionSquare size={15} /> Functions ({functions.length})
                </button>
                <button
                  onClick={() => { setTab("snippets"); setLibraryFilter("all"); setUseCaseFilters([]); closeForm(); }}
                  className={`flex items-center gap-1.5 px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
                    tab === "snippets" ? "border-brandTeal text-brandTeal" : "border-transparent text-slate-400 hover:text-slate-600"
                  }`}
                >
                  <Code2 size={15} /> Snippets ({snippets.length})
                </button>
              </div>

              {/* Controls */}
              <div className="mt-4 flex gap-2 flex-wrap items-center">
                <div className="relative flex-1 min-w-[200px]">
                  <Search size={15} className="absolute left-2.5 top-2.5 text-slate-400" />
                  <input
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    placeholder={tab === "functions" ? "Search functions..." : "Search snippets..."}
                    className="w-full rounded-md border border-slate-200 bg-white pl-8 pr-3 py-2 text-sm"
                  />
                </div>

                <div className="relative" ref={filterRef}>
                  <button
                    type="button"
                    onClick={() => setFilterOpen((o) => !o)}
                    className={`inline-flex items-center gap-1.5 rounded-md border px-3 py-2 text-sm font-medium transition-colors ${
                      activeFilterCount > 0
                        ? "border-brandTeal bg-brandTeal/10 text-brandTealDark"
                        : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
                    }`}
                  >
                    <Filter size={14} /> Filter
                    {activeFilterCount > 0 && (
                      <span className="ml-0.5 rounded-full bg-brandTeal text-white text-[10px] px-1.5 py-0.5 leading-none">
                        {activeFilterCount}
                      </span>
                    )}
                  </button>

                  {filterOpen && (
                    <div className="absolute right-0 z-10 mt-2 w-72 rounded-lg border border-slate-200 bg-white p-3 shadow-lg space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">Filters</span>
                        <button onClick={() => setFilterOpen(false)} className="text-slate-400 hover:text-slate-600">
                          <X size={14} />
                        </button>
                      </div>

                      <div>
                        <p className="text-xs font-medium text-slate-500 mb-1.5">Library</p>
                        <select
                          value={libraryFilter}
                          onChange={(e) => setLibraryFilter(e.target.value)}
                          className="w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm"
                        >
                          {librariesInUse.map((l) => (
                            <option key={l} value={l}>{l === "all" ? "All libraries" : l}</option>
                          ))}
                        </select>
                      </div>

                      <div>
                        <p className="text-xs font-medium text-slate-500 mb-1.5">Use case</p>
                        <MultiTagPicker selected={useCaseFilters} onToggle={toggleUseCaseFilter} />
                      </div>

                      {activeFilterCount > 0 && (
                        <button
                          onClick={() => { setLibraryFilter("all"); setUseCaseFilters([]); }}
                          className="text-xs text-slate-400 hover:text-slate-600 underline"
                        >
                          Clear all filters
                        </button>
                      )}
                    </div>
                  )}
                </div>

                <button
                  onClick={() => {
                    if (formMode === "add") closeForm();
                    else { setFormMode("add"); setEditingItem(null); }
                  }}
                  className="inline-flex items-center gap-1.5 rounded-md bg-brandTeal px-3 py-2 text-sm font-medium text-white hover:bg-brandTealDark"
                >
                  <Plus size={14} /> Add {tab === "functions" ? "function" : "snippet"}
                </button>
              </div>

              {/* Add/Edit form */}
              {formMode && (
                <div className="mt-4">
                  {tab === "functions" ? (
                    <FunctionForm
                      mode={formMode}
                      initial={formMode === "edit" ? editingItem : null}
                      onSubmit={handleSaveFunction}
                      onClose={closeForm}
                      libraries={libraries}
                      onAddLibrary={handleAddLibrary}
                    />
                  ) : (
                    <SnippetForm
                      mode={formMode}
                      initial={formMode === "edit" ? editingItem : null}
                      onSubmit={handleSaveSnippet}
                      onClose={closeForm}
                      libraries={libraries}
                      onAddLibrary={handleAddLibrary}
                    />
                  )}
                </div>
              )}

              {/* List */}
              <div className="mt-5 flex flex-col gap-4">
                {filtered.map((item) =>
                  tab === "functions" ? (
                    <FunctionCard key={item.id} item={item} onDelete={handleDelete} onEdit={startEdit} />
                  ) : (
                    <SnippetCard key={item.id} item={item} onDelete={handleDelete} onEdit={startEdit} />
                  )
                )}
              </div>

              {filtered.length === 0 && (
                <div className="mt-10 text-center text-sm text-slate-400">
                  Nothing matches those filters.
                </div>
              )}
            </>
          )}

          <p className="mt-8 text-center text-xs text-slate-400">
            Data lives in this session only — click <strong>Export JSON</strong> after edits and commit the file to your repo.
            Use <strong>Import</strong> next time to pick up where you left off.
          </p>
        </div>
      </div>
    </div>
  );
}
