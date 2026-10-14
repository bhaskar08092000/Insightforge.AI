"""InsightForge AI - Data Science & Business Analytics Platform.
Developed by Bhaskar Kewalramani | Portfolio single-file Streamlit app.
Run: streamlit run app.py
"""
import io
import warnings
from datetime import date
from typing import Any
import streamlit as st
import pandas as pd
import numpy as np
# Pre-declare optional deps as Any so Pylance doesn't flag None-attrs; runtime guards use HAS_* flags.
px: Any = None
go: Any = None
plt: Any = None
sns: Any = None
scipy_stats: Any = None
# sklearn placeholders (Any) to avoid possibly-unbound warnings when sklearn missing
train_test_split: Any = None
StandardScaler: Any = None
OneHotEncoder: Any = None
ColumnTransformer: Any = None
Pipeline: Any = None
SimpleImputer: Any = None
LinearRegression: Any = None
Ridge: Any = None
Lasso: Any = None
LogisticRegression: Any = None
DecisionTreeRegressor: Any = None
DecisionTreeClassifier: Any = None
RandomForestRegressor: Any = None
RandomForestClassifier: Any = None
GradientBoostingRegressor: Any = None
GradientBoostingClassifier: Any = None
KNeighborsClassifier: Any = None
KMeans: Any = None
PCA: Any = None
mean_absolute_error: Any = None
mean_squared_error: Any = None
r2_score: Any = None
accuracy_score: Any = None
precision_score: Any = None
recall_score: Any = None
f1_score: Any = None
confusion_matrix: Any = None
classification_report: Any = None
roc_curve: Any = None
auc: Any = None
silhouette_score: Any = None
try:
    import plotly.express as _px  # type: ignore
    import plotly.graph_objects as _go  # type: ignore
    px = _px; go = _go
    HAS_PLOTLY = True
except Exception:  # keep Any placeholders above
    HAS_PLOTLY = False
try:
    import matplotlib.pyplot as _plt  # type: ignore
    plt = _plt
    HAS_MPL=True
except Exception:
    HAS_MPL=False
try:
    import seaborn as _sns  # type: ignore
    sns = _sns
    HAS_SEABORN=True
except Exception:
    HAS_SEABORN=False
try:
    from sklearn.model_selection import train_test_split as _tts  # type: ignore
    from sklearn.preprocessing import StandardScaler as _ss, OneHotEncoder as _ohe  # type: ignore
    from sklearn.compose import ColumnTransformer as _ct  # type: ignore
    from sklearn.pipeline import Pipeline as _pl  # type: ignore
    from sklearn.impute import SimpleImputer as _si  # type: ignore
    from sklearn.linear_model import LinearRegression as _lr, Ridge as _rg, Lasso as _la, LogisticRegression as _logr  # type: ignore
    from sklearn.tree import DecisionTreeRegressor as _dtr, DecisionTreeClassifier as _dtc  # type: ignore
    from sklearn.ensemble import RandomForestRegressor as _rfr, RandomForestClassifier as _rfc, GradientBoostingRegressor as _gbr, GradientBoostingClassifier as _gbc  # type: ignore
    from sklearn.neighbors import KNeighborsClassifier as _knn  # type: ignore
    from sklearn.cluster import KMeans as _km  # type: ignore
    from sklearn.decomposition import PCA as _pca  # type: ignore
    from sklearn.metrics import mean_absolute_error as _mae, mean_squared_error as _mse, r2_score as _r2, accuracy_score as _acc, precision_score as _prec, recall_score as _rec, f1_score as _f1, confusion_matrix as _cm, classification_report as _cr, roc_curve as _roc, auc as _auc, silhouette_score as _sil  # type: ignore
    train_test_split=_tts; StandardScaler=_ss; OneHotEncoder=_ohe; ColumnTransformer=_ct; Pipeline=_pl; SimpleImputer=_si
    LinearRegression=_lr; Ridge=_rg; Lasso=_la; LogisticRegression=_logr
    DecisionTreeRegressor=_dtr; DecisionTreeClassifier=_dtc
    RandomForestRegressor=_rfr; RandomForestClassifier=_rfc; GradientBoostingRegressor=_gbr; GradientBoostingClassifier=_gbc
    KNeighborsClassifier=_knn; KMeans=_km; PCA=_pca
    mean_absolute_error=_mae; mean_squared_error=_mse; r2_score=_r2; accuracy_score=_acc; precision_score=_prec; recall_score=_rec; f1_score=_f1; confusion_matrix=_cm; classification_report=_cr; roc_curve=_roc; auc=_auc; silhouette_score=_sil
    HAS_SKLEARN=True
except Exception:
    HAS_SKLEARN=False
try:
    from scipy import stats as _scistats  # type: ignore
    scipy_stats = _scistats
    HAS_SCIPY=True
except Exception:
    HAS_SCIPY=False
try:
    import openpyxl  # noqa
    HAS_OPENPYXL=True
except Exception:
    HAS_OPENPYXL=False
warnings.filterwarnings("ignore")
st.set_page_config(page_title="InsightForge AI", page_icon="🔷", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>.main-header{font-size:2.2rem;font-weight:800;color:#0f2a44;margin-bottom:0}.sub-header{color:#4a6fa5}.kpi-card{background:linear-gradient(135deg,#fff 0%,#eef4ff 100%);border:1px solid #dbe6f7;border-radius:14px;padding:14px 16px;box-shadow:0 2px 10px rgba(15,42,68,.07)}.kpi-label{font-size:.78rem;color:#5b7290;text-transform:uppercase;letter-spacing:.06em}.kpi-value{font-size:1.55rem;font-weight:800;color:#0f2a44}.footer{text-align:center;color:#6b7d99;padding:18px 0 6px;font-size:.9rem;border-top:1px solid #e5edf7;margin-top:30px}.small-note{font-size:.85rem;color:#5b7290}</style>""", unsafe_allow_html=True)
APP_FOOTER="Developed by Bhaskar Kewalramani | Data Science & Business Analytics Portfolio"
def init_state():
    d={"original_df":None,"cleaned_df":None,"filtered_df":None,"predictions_df":None,"file_name":None,"file_size":None,"clean_log":[],"stat_results":None,"ml_results":None,"insights_list":[]}
    for k,v in d.items():
        if k not in st.session_state: st.session_state[k]=v
init_state()
PALETTES={"Plotly":None,"Viridis":"viridis","Blues":"Blues","Sunset":["#0f2a44","#2a7fff","#00c2a8","#ffb020","#ff5d5d"]}
@st.cache_data(show_spinner=False)
def load_data(file_bytes: bytes, filename: str):
    """Load CSV or Excel bytes into a DataFrame."""
    bio = io.BytesIO(file_bytes)
    fn = filename.lower()
    if fn.endswith(".csv"):
        try:
            return pd.read_csv(bio)
        except Exception:
            bio.seek(0)
            return pd.read_csv(bio, encoding="latin-1")
    elif fn.endswith((".xlsx", ".xls", ".xlsm")):
        return pd.read_excel(bio)
    raise ValueError("Unsupported format. Upload CSV, XLSX or XLS.")

def generate_sample_data(n: int = 600, seed: int = 42):
    """Create synthetic labelled demo sales dataset."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=n, freq="D")
    regions = ["North", "South", "East", "West"]
    products = ["Alpha Laptop", "Beta Phone", "Gamma Tablet", "Delta Monitor", "Epsilon Keyboard"]
    cmap = {"Alpha Laptop": "Electronics", "Beta Phone": "Electronics", "Gamma Tablet": "Electronics", "Delta Monitor": "Accessories", "Epsilon Keyboard": "Accessories"}
    segs = ["Consumer", "Corporate", "Small Business", "Enterprise"]
    df = pd.DataFrame({"Date": rng.choice(dates, n), "Region": rng.choice(regions, n),
        "Product": rng.choice(products, n), "Customer_Segment": rng.choice(segs, n),
        "Quantity": rng.integers(1, 20, n), "Discount": np.round(rng.uniform(0, .30, n), 2),
        "Customer_Rating": np.round(rng.uniform(2.5, 5.0, n), 1)})
    df["Category"] = df["Product"].map(cmap)
    bp = {"Alpha Laptop": 850, "Beta Phone": 520, "Gamma Tablet": 380, "Delta Monitor": 220, "Epsilon Keyboard": 60}
    df["Unit_Price"] = df["Product"].map(bp).astype(float) + rng.normal(0, 12, n)
    df["Sales"] = np.round(df["Unit_Price"] * df["Quantity"] * (1 - df["Discount"]), 2)
    df["Cost"] = np.round(df["Sales"] * rng.uniform(.55, .80, n), 2)
    df["Profit"] = np.round(df["Sales"] - df["Cost"], 2)
    df["Target_Sales"] = np.round(df["Sales"] * rng.uniform(.85, 1.15, n), 2)
    df["Profit_Margin"] = np.round(np.where(df["Sales"] != 0, df["Profit"] / df["Sales"] * 100, 0), 2)
    df["Sales_Variance"] = np.round(df["Sales"] - df["Target_Sales"], 2)
    df["Target_Achievement_Pct"] = np.round(np.where(df["Target_Sales"] != 0, df["Sales"] / df["Target_Sales"] * 100, 0), 2)
    df["Date"] = pd.to_datetime(df["Date"])
    return df.sort_values("Date").reset_index(drop=True)

def detect_column_types(df):
    """Classify columns into numeric/categorical/datetime/boolean/text."""
    num, cat, dt, bl, tx = [], [], [], [], []
    for c in df.columns:
        s = df[c]
        if pd.api.types.is_bool_dtype(s): bl.append(c)
        elif pd.api.types.is_datetime64_any_dtype(s): dt.append(c)
        elif pd.api.types.is_numeric_dtype(s): num.append(c)
        else:
            try:
                co = pd.to_datetime(s.dropna().astype(str).head(40), errors="coerce")
                if len(s.dropna()) > 0 and co.notna().mean() > .8:
                    dt.append(c); continue
            except Exception: pass
            tx.append(c) if (s.dtype == object and len(s) and s.astype(str).str.len().mean() > 60) else cat.append(c)
    return {"numeric": num, "categorical": cat, "datetime": dt, "boolean": bl, "text": tx}

def calculate_data_quality(df):
    """Return 0-100 quality score with details."""
    if df is None or df.empty: return {"score": 0, "details": {}}
    miss = df.isna().sum().sum() / max(df.size, 1) * 100
    dup = df.duplicated().mean() * 100 if len(df) else 0
    const = sum(1 for c in df.columns if df[c].nunique(dropna=True) <= 1)
    score = float(np.clip(round(100 - (miss * 1.2 + dup * 1.0 + const / max(len(df.columns), 1) * 100 * .5), 1), 0, 100))
    return {"score": score, "details": {"missing_pct": round(float(miss), 2), "duplicate_pct": round(float(dup), 2), "constant_cols": int(const)}}

def get_active_df():
    if st.session_state.get("filtered_df") is not None: return st.session_state["filtered_df"]
    if st.session_state.get("cleaned_df") is not None: return st.session_state["cleaned_df"]
    return st.session_state.get("original_df")

def kpi_card(label, value, delta=None, up_good=True):
    d = ""
    if delta is not None:
        cls = "kpi-delta-up" if ((delta >= 0) == up_good) else "kpi-delta-down"
        arrow = "▲" if delta >= 0 else "▼"
        d = f"<div class='{cls}'>{arrow} {delta:+.1f}%</div>"
    st.markdown(f"<div class='kpi-card'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div>{d}</div>", unsafe_allow_html=True)

def to_snake(name: str):
    import re
    s = re.sub(r"[^0-9a-zA-Z]+", "_", str(name).strip()).strip("_").lower()
    return re.sub(r"_+", "_", s) or "col"

def render_home():
    """Landing page with intro, features and instructions."""
    st.markdown("<p class='main-header'>🔷 InsightForge AI</p>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Data Science & Business Analytics Platform — upload a file or try synthetic demo data.</p>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("Modules", "14")
    with c2: kpi_card("Chart Types", "16+")
    with c3: kpi_card("ML Models", "11")
    with c4: kpi_card("API Key", "Not needed")
    st.info("👈 Upload a CSV/Excel file in the sidebar, or click **Load sample data**. Then use filters and open any module.")
    t1, t2, t3 = st.tabs(["✨ Features", "🧭 How to use", "🏢 Use cases & stack"])
    with t1:
        a, b, c = st.columns(3)
        a.markdown("**📤 Profiling**\n- CSV/XLSX/XLS\n- Data dictionary\n- Quality score 0–100")
        b.markdown("**🧹 Cleaning**\n- Duplicates, outliers (IQR/Z)\n- Type fixes, renames\n- Undo to original")
        c.markdown("**📊 EDA + Business**\n- 16+ Plotly charts\n- Pareto, ABC, trends\n- KPI dashboard")
        a.markdown("**📈 Stats + ML**\n- t-tests, ANOVA, chi-square\n- Regression & classification\n- Clustering + forecasting")
        b.markdown("**🔮 Planning**\n- What-if scenarios\n- Rule-based insights\n- HTML report + downloads")
        c.markdown("**🔒 Privacy**\n- Session-only processing\n- No external AI API\n- No paid services")
    with t2:
        st.markdown("1. Upload file or **Load sample data**.\n2. Review **Data Profile**.\n3. Clean in **Cleaning**.\n4. Apply sidebar filters.\n5. Explore EDA → Business → KPIs → Stats → ML → Clusters → Forecast → What-If → Insights.\n6. Download everything in **Reports**.")
        st.caption("Supported: .csv, .xlsx, .xls (openpyxl). Large files get sampled for heavy charts.")
    with t3:
        st.markdown("**Use cases:** sales review, regional performance, target variance, customer segmentation, demand forecast, quality audit.")
        st.markdown("**Stack:** Streamlit, pandas, numpy, plotly, matplotlib, seaborn, scikit-learn, scipy, openpyxl.")
        st.warning("🔒 Privacy: uploaded data is processed in-memory during this session only. Nothing is sent to external AI services.")
    st.markdown(f"<div class='footer'>{APP_FOOTER}</div>", unsafe_allow_html=True)

def render_data_profile(df, ctypes):
    """Dataset overview, dictionary, stats and quality."""
    st.header("📤 Data Upload & Profiling")
    st.caption("File summary, column dictionary, samples and quality score.")
    q = calculate_data_quality(df)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: kpi_card("Rows", f"{len(df):,}")
    with c2: kpi_card("Columns", f"{df.shape[1]}")
    with c3: kpi_card("Missing cells", f"{int(df.isna().sum().sum()):,}")
    with c4: kpi_card("Duplicates", f"{int(df.duplicated().sum()):,}")
    with c5: kpi_card("Quality", f"{q['score']}/100")
    st.progress(min(max(q["score"] / 100, 0), 1))
    st.write(f"**File:** {st.session_state.get('file_name') or 'synthetic demo'} | **Size:** {(st.session_state.get('file_size') or 0)/1024:.1f} KB | **Memory:** {df.memory_usage(deep=True).sum()/1024:.1f} KB")
    st.write(f"Numeric: {len(ctypes['numeric'])} | Categorical: {len(ctypes['categorical'])} | Datetime: {len(ctypes['datetime'])} | Boolean: {len(ctypes['boolean'])} | Text: {len(ctypes['text'])}")
    dd = pd.DataFrame([{"Column": c, "Detected Type": ("numeric" if c in ctypes["numeric"] else "categorical" if c in ctypes["categorical"] else "datetime" if c in ctypes["datetime"] else "boolean" if c in ctypes["boolean"] else "text"),
        "Dtype": str(df[c].dtype), "Non-null": int(df[c].notna().sum()), "Missing %": round(df[c].isna().mean()*100, 2),
        "Unique": int(df[c].nunique(dropna=True)), "Example": ("" if df[c].dropna().empty else str(df[c].dropna().iloc[0])[:60])} for c in df.columns])
    t1, t2, t3, t4 = st.tabs(["📖 Dictionary", "👀 Samples", "📊 Describe", "🧪 Missing"])
    with t1: st.dataframe(dd, use_container_width=True)
    with t2:
        st.write("First 5"); st.dataframe(df.head(), use_container_width=True)
        st.write("Last 5"); st.dataframe(df.tail(), use_container_width=True)
        st.write("Random 5"); st.dataframe(df.sample(min(5, len(df)), random_state=7), use_container_width=True)
    with t3:
        st.write("Numeric"); st.dataframe(df[ctypes["numeric"]].describe().T if ctypes["numeric"] else pd.DataFrame(), use_container_width=True)
        st.write("Categorical"); st.dataframe(df[ctypes["categorical"]].describe().T if ctypes["categorical"] else pd.DataFrame(), use_container_width=True)
        st.write("Unique counts"); st.dataframe(df.nunique().rename("unique").to_frame(), use_container_width=True)
    with t4:
        m = pd.DataFrame({"missing": df.isna().sum(), "missing_pct": (df.isna().mean()*100).round(2)}).sort_values("missing", ascending=False)
        st.dataframe(m, use_container_width=True)
        if HAS_PLOTLY and m["missing"].sum() > 0:
            st.plotly_chart(px.bar(m.reset_index().rename(columns={"index": "column"}), x="column", y="missing", title="Missing values per column"), use_container_width=True)

def render_cleaning(df, ctypes):
    """Interactive cleaning with before/after tracking."""
    st.header("🧹 Data Cleaning")
    st.caption("Working copy is edited; original preserved for Undo.")
    if st.session_state.get("cleaned_df") is None:
        st.session_state["cleaned_df"] = df.copy()
    work = st.session_state["cleaned_df"]
    b_rows, b_miss, b_dup = len(df), int(df.isna().sum().sum()), int(df.duplicated().sum())
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🧹 Remove duplicates", key="rm_dup"):
            n = int(work.duplicated().sum()); work = work.drop_duplicates()
            st.session_state["clean_log"].append(f"Removed {n} duplicate rows.")
            st.session_state["cleaned_df"] = work; st.success(f"Removed {n}.")
    with c2:
        cols_drop = st.multiselect("Remove columns", list(work.columns), key="drop_cols")
        if st.button("Drop columns", key="drop_btn") and cols_drop:
            work = work.drop(columns=cols_drop)
            st.session_state["clean_log"].append(f"Dropped: {cols_drop}")
            st.session_state["cleaned_df"] = work; st.success("Dropped.")
    with c3:
        if st.button("↩️ Undo (restore original)", key="undo_btn"):
            st.session_state["cleaned_df"] = df.copy(); st.session_state["filtered_df"] = None
            st.session_state["clean_log"].append("Restored original.")
            work = st.session_state["cleaned_df"]; st.success("Restored.")
    with st.expander("✏️ Rename / tidy columns", expanded=True):
        a, b = st.columns(2)
        with a:
            rc = st.selectbox("Column to rename", list(work.columns), key="rn_col")
            nv = st.text_input("New name", value=str(rc), key="rn_new")
            if st.button("Rename", key="rn_btn") and nv and nv != rc:
                work = work.rename(columns={rc: nv}); st.session_state["cleaned_df"] = work
                st.session_state["clean_log"].append(f"Renamed {rc}->{nv}"); st.success("Renamed.")
        with b:
            if st.button("Trim spaces in names", key="trim_names"):
                work.columns = [str(c).strip() for c in work.columns]
                st.session_state["cleaned_df"] = work; st.success("Trimmed.")
            if st.button("snake_case names", key="snake_btn"):
                work.columns = [to_snake(c) for c in work.columns]
                st.session_state["cleaned_df"] = work; st.success("Converted.")
    with st.expander("🧪 Missing values", expanded=True):
        num_cols = work.select_dtypes(include=np.number).columns.tolist()
        m1, m2 = st.columns(2)
        with m1:
            nc = st.selectbox("Numeric col", num_cols or ["(none)"], key="fill_num")
            strat = st.selectbox("Strategy", ["mean", "median", "mode", "custom", "drop rows"], key="fill_strat")
            cv = st.number_input("Custom value", value=0.0, key="fill_cv")
            if st.button("Apply numeric fill", key="fill_num_btn") and nc != "(none)":
                if strat == "drop rows": work = work.dropna(subset=[nc])
                else:
                    v = {"mean": work[nc].mean(), "median": work[nc].median(), "mode": work[nc].mode().iloc[0] if not work[nc].mode().empty else 0, "custom": cv}[strat]
                    work[nc] = work[nc].fillna(v)
                st.session_state["cleaned_df"] = work; st.success("Applied.")
        with m2:
            cat_cols = [c for c in work.columns if c not in num_cols]
            cc = st.selectbox("Categorical col", cat_cols or ["(none)"], key="fill_cat")
            cs = st.selectbox("Cat strategy", ["mode", "custom", "drop rows"], key="fill_cstrat")
            cvc = st.text_input("Custom category", value="Unknown", key="fill_cval")
            if st.button("Apply cat fill", key="fill_cat_btn") and cc != "(none)":
                if cs == "drop rows": work = work.dropna(subset=[cc])
                else:
                    v = work[cc].mode().iloc[0] if (cs == "mode" and not work[cc].mode().empty) else cvc
                    work[cc] = work[cc].fillna(v)
                st.session_state["cleaned_df"] = work; st.success("Applied.")
        if st.button("Drop ALL rows with any missing", key="dropna_all"):
            work = work.dropna(); st.session_state["cleaned_df"] = work; st.success("Dropped NA rows.")
    work = st.session_state["cleaned_df"]
    with st.expander("📉 Outliers (IQR / Z-score)", expanded=True):
        ncol = st.selectbox("Numeric column", work.select_dtypes(include=np.number).columns.tolist() or ["(none)"], key="out_col")
        meth = st.radio("Method", ["IQR", "Z-score"], horizontal=True, key="out_meth")
        act = st.radio("Action", ["Detect only", "Remove outliers"], horizontal=True, key="out_act")
        if st.button("Run outlier check", key="out_btn") and ncol != "(none)":
            s = pd.to_numeric(work[ncol], errors="coerce").dropna()
            if meth == "IQR":
                q1, q3 = s.quantile(.25), s.quantile(.75); iqr = q3 - q1
                lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            else:
                mu, sd = s.mean(), s.std(ddof=0) or 1; lo, hi = mu - 3 * sd, mu + 3 * sd
            mask = (pd.to_numeric(work[ncol], errors="coerce") < lo) | (pd.to_numeric(work[ncol], errors="coerce") > hi)
            st.write(f"Bounds [{lo:.2f}, {hi:.2f}] — outliers: {int(mask.sum())}")
            if act == "Remove outliers" and mask.sum() > 0:
                work = work.loc[~mask.fillna(False)]; st.session_state["cleaned_df"] = work
                st.session_state["clean_log"].append(f"Removed {int(mask.sum())} outliers from {ncol}")
                st.success("Removed.")
    with st.expander("📅 Dates & types"):
        dcol = st.selectbox("Parse date col", ["(none)"] + list(work.columns), key="dt_col")
        if st.button("To datetime", key="dt_btn") and dcol != "(none)":
            try:
                work[dcol] = pd.to_datetime(work[dcol], errors="coerce")
                st.session_state["cleaned_df"] = work; st.success("Converted.")
            except Exception as e: st.error(f"Failed: {e}")
    w = st.session_state["cleaned_df"]
    st.subheader("Before → After")
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Rows", f"{len(w):,} (was {b_rows:,})")
    with k2: kpi_card("Missing", f"{int(w.isna().sum().sum()):,} (was {b_miss:,})")
    with k3: kpi_card("Duplicates", f"{int(w.duplicated().sum()):,} (was {b_dup:,})")
    with k4: kpi_card("Columns", f"{w.shape[1]}")
    st.write("**Activity log**"); st.write(st.session_state["clean_log"] or "No actions yet.")
    st.dataframe(w.head(20), use_container_width=True)

def render_eda(df, ctypes, palette):
    """Interactive univariate/bivariate/multivariate charts."""
    st.header("📊 Exploratory Data Analysis")
    st.caption("Pick axes, grouping and chart type. Invalid combos are blocked with guidance.")
    if not HAS_PLOTLY:
        st.error("Plotly is not installed. Run: pip install plotly"); return
    all_cols = list(df.columns)
    c1, c2, c3, c4 = st.columns(4)
    with c1: x = st.selectbox("X-axis", all_cols, key="eda_x")
    with c2: y = st.selectbox("Y-axis", ["(none)"] + all_cols, key="eda_y")
    with c3: color = st.selectbox("Color/group", ["(none)"] + all_cols, key="eda_c")
    with c4: chart = st.selectbox("Chart", ["Histogram", "Box", "Violin", "Bar", "Line", "Area", "Scatter", "Bubble", "Pie", "Donut", "Heatmap/Corr", "Treemap", "Sunburst", "Funnel", "Waterfall"], key="eda_t")
    agg = st.selectbox("Aggregation", ["sum", "mean", "median", "count", "min", "max"], key="eda_agg")
    topn = st.slider("Top N categories", 3, 30, 10, key="eda_topn")
    title = st.text_input("Chart title", value=f"{chart}: {x}" + (f" vs {y}" if y != "(none)" else ""), key="eda_title")
    seq = PALETTES.get(palette)
    plot_df = df if len(df) <= 5000 else df.sample(5000, random_state=1)
    if len(df) > 5000: st.warning("Large dataset sampled to 5,000 rows for chart speed.")
    try:
        fig = None
        xn, yn = (x in ctypes["numeric"]), (y in ctypes["numeric"] if y != "(none)" else False)
        if chart == "Histogram":
            if not xn: st.warning("Histogram needs numeric X."); return
            fig = px.histogram(plot_df, x=x, color=None if color == "(none)" else color, title=title, color_discrete_sequence=seq)
        elif chart in ("Box", "Violin"):
            if y == "(none)": st.warning("Box/Violin need a Y column."); return
            if not yn: st.warning("Y must be numeric."); return
            f = px.box if chart == "Box" else px.violin
            fig = f(plot_df, x=x, y=y, color=None if color == "(none)" else color, title=title, color_discrete_sequence=seq)
        elif chart == "Bar":
            if y == "(none)":
                vc = plot_df[x].value_counts().head(topn).reset_index(); vc.columns = [x, "count"]
                fig = px.bar(vc, x=x, y="count", title=title, color_discrete_sequence=seq)
            else:
                if not yn: st.warning("Y must be numeric for aggregation."); return
                g = plot_df.groupby(x, dropna=False)[y].agg(agg if agg != "count" else "count").reset_index()
                g = g.sort_values(y, ascending=False).head(topn)
                fig = px.bar(g, x=x, y=y, title=title, color_discrete_sequence=seq)
        elif chart in ("Line", "Area"):
            if y == "(none)" or not yn: st.warning("Line/Area need numeric Y."); return
            d = plot_df.sort_values(x) if x in ctypes["datetime"] else plot_df.groupby(x, dropna=False)[y].mean(numeric_only=True).reset_index()
            fig = px.line(d, x=x, y=y, title=title) if chart == "Line" else px.area(d, x=x, y=y, title=title)
        elif chart in ("Scatter", "Bubble"):
            if y == "(none)" or not (xn and yn): st.warning("Scatter/Bubble need numeric X and Y."); return
            kw = {} if color == "(none)" else {"color": color}
            if chart == "Bubble": kw["size"] = y
            fig = px.scatter(plot_df, x=x, y=y, title=title, **kw)
        elif chart in ("Pie", "Donut"):
            vc = plot_df[x].value_counts().head(topn).reset_index(); vc.columns = [x, "count"]
            fig = px.pie(vc, names=x, values="count", title=title, hole=.45 if chart == "Donut" else 0)
        elif chart == "Heatmap/Corr":
            nums = df[ctypes["numeric"]]
            if nums.shape[1] < 2: st.warning("Need 2+ numeric columns."); return
            fig = px.imshow(nums.corr(numeric_only=True), text_auto=True, title=title or "Correlation matrix", aspect="auto")
        elif chart in ("Treemap", "Sunburst"):
            if y == "(none)" or not yn: st.warning("Treemap/Sunburst need numeric Y."); return
            path = [x] + ([color] if color != "(none)" else [])
            f = px.treemap if chart == "Treemap" else px.sunburst
            fig = f(plot_df, path=path, values=y, title=title)
        elif chart == "Funnel":
            g = plot_df.groupby(x, dropna=False).size().reset_index(name="count").sort_values("count", ascending=False).head(topn)
            fig = px.funnel(g, x="count", y=x, title=title)
        elif chart == "Waterfall":
            if not xn: st.warning("Waterfall needs numeric X."); return
            s = plot_df[x].dropna().head(20)
            fig = go.Figure(go.Waterfall(x=list(range(len(s))), y=s.tolist(), connector={"line": {"color": "gray"}}))
            fig.update_layout(title=title)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        with st.expander("Pairwise relationships (sample)"):
            nums = ctypes["numeric"][:4]
            if len(nums) >= 2:
                st.plotly_chart(px.scatter_matrix(plot_df[nums].dropna().head(500)), use_container_width=True)
            else: st.info("Need 2+ numeric columns.")
        with st.expander("Correlation table"):
            if ctypes["numeric"]: st.dataframe(df[ctypes["numeric"]].corr(numeric_only=True).round(3), use_container_width=True)
    except Exception as e:
        st.error(f"Chart failed: {e}. Try different columns.")
def render_business(df, ctypes):
    """Adaptive business dashboard with Pareto, ABC and rule insights."""
    st.header("💼 Business Analysis")
    st.caption("Select business roles for your columns. All insights are rule-based, no AI API.")
    nums, cats, dts = ctypes["numeric"], ctypes["categorical"], ctypes["datetime"]
    if not nums or not cats:
        st.warning("Need at least 1 numeric and 1 categorical column."); return
    c1, c2, c3 = st.columns(3)
    with c1: mcol = st.selectbox("Main metric", nums, key="b_metric")
    with c2: cat = st.selectbox("Category column", cats, key="b_cat")
    with c3: dcol = st.selectbox("Date column", ["(none)"] + dts, key="b_date")
    c4, c5, c6 = st.columns(3)
    with c4: seg = st.selectbox("Region/segment", ["(none)"] + [c for c in cats if c != cat], key="b_seg")
    with c5: acol = st.selectbox("Actual col", ["(none)"] + nums, key="b_act")
    with c6: tcol = st.selectbox("Target col", ["(none)"] + [n for n in nums if n != acol], key="b_tgt")
    s = pd.to_numeric(df[mcol], errors="coerce").dropna()
    tot, avg, mn, mx = s.sum(), s.mean(), s.min(), s.max()
    k1, k2, k3, k4 = st.columns(4)
    with k1: kpi_card("Records", f"{len(df):,}")
    with k2: kpi_card(f"Total {mcol}", f"{tot:,.0f}")
    with k3: kpi_card(f"Avg {mcol}", f"{avg:,.1f}")
    with k4: kpi_card("Min / Max", f"{mn:,.0f} / {mx:,.0f}")
    g = df.groupby(cat)[mcol].sum(numeric_only=True).sort_values(ascending=False)
    share = (g / g.sum() * 100).round(2) if g.sum() else g
    top, bot = g.head(5), g.tail(5)
    st.subheader("Top / Bottom categories")
    t1, t2 = st.columns(2)
    with t1: st.dataframe(top.rename("total").to_frame().assign(share_pct=share.head(5)), use_container_width=True)
    with t2: st.dataframe(bot.rename("total").to_frame().assign(share_pct=share.tail(5)), use_container_width=True)
    if HAS_PLOTLY:
        st.plotly_chart(px.bar(top.reset_index(), x=cat, y=mcol, title=f"Top categories by {mcol}"), use_container_width=True)
        pareto = g.reset_index(); pareto["cum_pct"] = pareto[mcol].cumsum() / pareto[mcol].sum() * 100
        fig = go.Figure([go.Bar(x=pareto[cat], y=pareto[mcol], name=mcol), go.Scatter(x=pareto[cat], y=pareto["cum_pct"], name="Cum %", yaxis="y2")])
        fig.update_layout(title="Pareto analysis", yaxis2=dict(overlaying="y", side="right", range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)
    abc = pd.DataFrame({"total": g, "cum_pct": (g.cumsum() / g.sum() * 100).round(1)})
    abc["ABC"] = pd.cut(abc["cum_pct"], [0, 80, 95, 100.01], labels=["A", "B", "C"])
    st.write("**ABC classification** (A≈80% value, B≈15%, C≈5%)"); st.dataframe(abc, use_container_width=True)
    obs = []
    if len(g):
        obs.append(f"🏆 Highest {cat}: **{g.index[0]}** ({g.iloc[0]:,.0f}, {share.iloc[0]:.1f}% of total).")
        obs.append(f"⚠️ Lowest {cat}: **{g.index[-1]}** ({g.iloc[-1]:,.0f}, {share.iloc[-1]:.1f}%).")
        hhi = float(((share / 100) ** 2).sum())
        obs.append(f"🎯 Concentration (HHI): {hhi:.3f} — {'high concentration risk' if hhi > .25 else 'moderate' if hhi > .15 else 'diversified'}. Top item holds {share.iloc[0]:.1f}%.")
    if dcol != "(none)":
        try:
            dd = df.copy(); dd[dcol] = pd.to_datetime(dd[dcol], errors="coerce")
            dd = dd.dropna(subset=[dcol]).sort_values(dcol)
            ts = dd.set_index(dcol).resample("M")[mcol].sum(numeric_only=True)
            if len(ts) >= 2:
                ch = (ts.iloc[-1] - ts.iloc[-2]) / abs(ts.iloc[-2]) * 100 if ts.iloc[-2] else 0
                obs.append(f"📈 Last month {mcol}: {ts.iloc[-1]:,.0f} vs {ts.iloc[-2]:,.0f} ({ch:+.1f}% MoM).")
                if HAS_PLOTLY: st.plotly_chart(px.line(ts.reset_index(), x=dcol, y=mcol, title=f"Monthly trend — {mcol}"), use_container_width=True)
        except Exception as e: st.warning(f"Trend skipped: {e}")
    if acol != "(none)" and tcol != "(none)":
        a, t = pd.to_numeric(df[acol], errors="coerce").sum(), pd.to_numeric(df[tcol], errors="coerce").sum()
        var = a - t; ach = (a / t * 100) if t else 0
        obs.append(f"🎯 Actual vs Target: actual {a:,.0f} vs target {t:,.0f} → variance {var:+,.0f} ({ach:.1f}% achieved).")
        if HAS_PLOTLY:
            st.plotly_chart(px.bar(pd.DataFrame({"Type": ["Actual", "Target"], "Value": [a, t]}), x="Type", y="Value", title="Actual vs Target"), use_container_width=True)
    if seg != "(none)":
        sg = df.groupby(seg)[mcol].sum(numeric_only=True).sort_values(ascending=False)
        obs.append(f"🗺️ Top {seg}: **{sg.index[0]}** ({sg.iloc[0]:,.0f}); bottom: **{sg.index[-1]}** ({sg.iloc[-1]:,.0f}).")
        st.write(f"**Segmentation by {seg}**"); st.dataframe(sg.rename("total").to_frame(), use_container_width=True)
    st.subheader("📝 Business observations")
    for o in obs: st.markdown("- " + o)
    st.session_state["insights_list"] = obs
    with st.expander("Top 5 / Bottom 5 records"):
        st.write(df.nlargest(min(5, len(df)), mcol)); st.write(df.nsmallest(min(5, len(df)), mcol))

def render_kpi_dashboard(df, ctypes):
    """Executive KPI cards, trends and breakdowns."""
    st.header("📌 KPI Dashboard")
    nums, cats, dts = ctypes["numeric"], ctypes["categorical"], ctypes["datetime"]
    if not nums: st.warning("No numeric columns."); return
    m = st.selectbox("KPI metric", nums, key="kpi_m")
    c = st.selectbox("Breakdown", ["(none)"] + cats, key="kpi_c")
    d = st.selectbox("Date", ["(none)"] + dts, key="kpi_d")
    s = pd.to_numeric(df[m], errors="coerce").dropna()
    tot, avg = s.sum(), s.mean()
    delta = None
    if d != "(none)":
        try:
            t = df.assign(_d=pd.to_datetime(df[d], errors="coerce")).dropna(subset=["_d"]).sort_values("_d")
            t = t.set_index("_d").resample("M")[m].sum(numeric_only=True)
            if len(t) >= 2 and t.iloc[-2]: delta = float((t.iloc[-1] - t.iloc[-2]) / abs(t.iloc[-2]) * 100)
        except Exception: pass
    k1, k2, k3 = st.columns(3)
    with k1: kpi_card(f"Total {m}", f"{tot:,.0f}", delta)
    with k2: kpi_card(f"Average {m}", f"{avg:,.1f}")
    with k3: kpi_card("Records", f"{len(df):,}")
    if HAS_PLOTLY:
        if d != "(none)":
            try:
                t = df.assign(_d=pd.to_datetime(df[d], errors="coerce")).dropna(subset=["_d"]).sort_values("_d")
                t = t.set_index("_d").resample("M")[m].sum(numeric_only=True).reset_index()
                st.plotly_chart(px.line(t, x="_d", y=m, title=f"Monthly {m}"), use_container_width=True)
            except Exception as e: st.warning(f"Trend failed: {e}")
        if c != "(none)":
            g = df.groupby(c)[m].sum(numeric_only=True).sort_values(ascending=False).reset_index()
            st.plotly_chart(px.bar(g.head(15), x=c, y=m, title=f"{m} by {c}"), use_container_width=True)
            st.plotly_chart(px.pie(g.head(8), names=c, values=m, title="Contribution (top 8)", hole=.4), use_container_width=True)
    st.success(f"Management summary: total {m} is {tot:,.0f} across {len(df):,} records (avg {avg:,.1f})." + (f" MoM change {delta:+.1f}%." if delta is not None else ""))
def render_statistics(df, ctypes):
    """Descriptives, correlations and hypothesis tests."""
    st.header("📈 Statistical Analysis")
    st.caption("Plain-English results with hypotheses, p-values and business meaning.")
    nums, cats = ctypes["numeric"], ctypes["categorical"]
    if not nums: st.warning("No numeric columns."); return
    col = st.selectbox("Column", nums, key="st_col")
    s = pd.to_numeric(df[col], errors="coerce").dropna()
    alpha = st.selectbox("Significance α", [.01, .05, .10], index=1, key="st_a")
    if len(s) < 3: st.warning("Not enough data."); return
    desc = {"mean": s.mean(), "median": s.median(), "mode": s.mode().iloc[0] if not s.mode().empty else np.nan,
        "var": s.var(), "std": s.std(), "min": s.min(), "max": s.max(), "range": s.max() - s.min(),
        "q1": s.quantile(.25), "q3": s.quantile(.75), "iqr": s.quantile(.75) - s.quantile(.25),
        "skew": s.skew(), "kurt": s.kurt()}
    st.dataframe(pd.Series(desc).round(3).rename(col).to_frame(), use_container_width=True)
    if HAS_SCIPY:
        try:
            if len(s) >= 8:
                w, p = scipy_stats.shapiro(s.sample(min(5000, len(s)), random_state=1))
                st.write(f"**Normality (Shapiro):** W={w:.3f}, p={p:.4f} → {'likely normal' if p > alpha else 'not normal'} (H0: data is normal).")
            if len(s) >= 2:
                ci = scipy_stats.t.interval(.95, len(s) - 1, loc=s.mean(), scale=scipy_stats.sem(s))
                st.write(f"**95% CI for mean:** [{ci[0]:,.2f}, {ci[1]:,.2f}]")
        except Exception as e: st.warning(f"Advanced stats skipped: {e}")
    else: st.info("Install scipy for normality/CI tests: pip install scipy")
    t1, t2, t3 = st.tabs(["🔗 Correlations", "🧪 t-test / ANOVA", "📊 Chi-square / Regression"])
    with t1:
        if len(nums) >= 2:
            m = st.selectbox("Method", ["pearson", "spearman"], key="corr_m")
            st.dataframe(df[nums].corr(method=m, numeric_only=True).round(3), use_container_width=True)
            if HAS_PLOTLY: st.plotly_chart(px.imshow(df[nums].corr(method=m, numeric_only=True), text_auto=True, title=f"{m} correlation"), use_container_width=True)
    with t2:
        if HAS_SCIPY:
            c2 = st.selectbox("Group col (t-test/ANOVA)", ["(none)"] + cats, key="tt_g")
            try:
                if c2 != "(none)":
                    grps = [pd.to_numeric(df.loc[df[c2] == g, col], errors="coerce").dropna() for g in df[c2].dropna().unique()[:6]]
                    grps = [g for g in grps if len(g) >= 2]
                    if len(grps) == 2:
                        _tt = scipy_stats.ttest_ind(grps[0], grps[1], equal_var=False)
                        t, p = float(_tt[0]), float(_tt[1])
                        st.write(f"**Independent t-test** H0: equal means. t={t:.3f}, p={p:.4f} → {'reject H0 (different)' if p < alpha else 'keep H0 (no difference)'}.")
                        st.caption("Business: p<α means the two groups differ enough to act on.")
                    elif len(grps) > 2:
                        _fw = scipy_stats.f_oneway(*grps)
                        f, p = float(_fw[0]), float(_fw[1])
                        st.write(f"**One-way ANOVA** H0: all group means equal. F={f:.3f}, p={p:.4f} → {'reject H0' if p < alpha else 'keep H0'}.")
                    else: st.info("Need 2+ groups with 2+ values each.")
                else: st.info("Pick a group column, or use descriptives above.")
            except Exception as e: st.error(f"Test failed: {e}")
        else: st.info("Install scipy.")
    with t3:
        if HAS_SCIPY:
            c3a = st.selectbox("Cat A", cats or ["(none)"], key="chi_a")
            c3b = st.selectbox("Cat B", [c for c in cats if c != c3a] or ["(none)"], key="chi_b")
            if c3a != "(none)" and c3b != "(none)":
                try:
                    ct = pd.crosstab(df[c3a], df[c3b])
                    _ch = scipy_stats.chi2_contingency(ct)
                    chi2, p, dof = float(_ch[0]), float(_ch[1]), int(_ch[2])
                    st.write(f"**Chi-square** H0: independent. χ²={chi2:.2f}, p={p:.4f} → {'associated' if p < alpha else 'independent'}.")
                except Exception as e: st.error(f"Chi-square failed: {e}")
            rx = st.selectbox("Regressor X", nums, key="reg_x")
            if st.button("Run simple regression", key="reg_btn"):
                try:
                    x, y = pd.to_numeric(df[rx], errors="coerce"), s
                    msk = x.notna() & y.notna(); x, y = x[msk], y[msk]
                    sl, ic, r, p, se = (float(v) for v in scipy_stats.linregress(x, y))
                    st.write(f"y={ic:.2f}+{sl:.4f}·x, R²={r**2:.3f}, p={p:.4f}. Business: " + ("X predicts Y." if p < alpha else "no reliable linear link."))
                    if HAS_PLOTLY: st.plotly_chart(px.scatter(pd.DataFrame({"x": x, "y": y}), x="x", y="y", trendline="ols", title=f"{col} vs {rx}"), use_container_width=True)
                except Exception as e: st.error(f"Regression failed: {e}")
def build_preprocessor(X):
    """Numeric impute+scale, categorical impute+onehot (capped)."""
    nums = X.select_dtypes(include=np.number).columns.tolist()
    cats = [c for c in X.columns if c not in nums]
    kept = []
    for c in cats:
        if X[c].nunique(dropna=True) > 50:
            kept.append(c)
    cats = [c for c in cats if c not in kept]
    if kept: st.warning(f"High-cardinality dropped: {kept}")
    trans = []
    if nums: trans.append(("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler())]), nums))
    if cats: trans.append(("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]), cats))
    return ColumnTransformer(trans) if trans else "passthrough"

def render_ml(df, ctypes):
    """Regression/classification with comparison and plots."""
    st.header("🤖 Machine Learning")
    if not HAS_SKLEARN: st.error("Install scikit-learn: pip install scikit-learn"); return
    nums = ctypes["numeric"] + ctypes["boolean"]
    allc = list(df.columns)
    tgt = st.selectbox("Target", allc, key="ml_t")
    feats = st.multiselect("Features (default: all except target)", [c for c in allc if c != tgt], key="ml_f")
    if not feats: feats = [c for c in allc if c != tgt]
    if tgt in feats: feats = [f for f in feats if f != tgt]; st.warning("Target removed from features (leakage guard).")
    y = df[tgt]; is_num = pd.api.types.is_numeric_dtype(y) and y.nunique(dropna=True) > 10
    mode = st.radio("Mode", ["Auto", "Regression", "Classification"], horizontal=True, key="ml_mode")
    task = ("regression" if is_num else "classification") if mode == "Auto" else mode.lower()
    st.write(f"Detected task: **{task}** (override with Mode).")
    ts = st.slider("Test size", .1, .4, .2, key="ml_ts")
    rs = st.number_input("Random state", value=42, key="ml_rs")
    if task == "regression":
        models = {"Linear": LinearRegression(), "Ridge": Ridge(), "Lasso": Lasso(), "DecisionTree": DecisionTreeRegressor(random_state=rs), "RandomForest": RandomForestRegressor(n_estimators=100, random_state=rs), "GradBoost": GradientBoostingRegressor(random_state=rs)}
    else:
        models = {"Logistic": LogisticRegression(max_iter=1000), "KNN": KNeighborsClassifier(), "DecisionTree": DecisionTreeClassifier(random_state=rs), "RandomForest": RandomForestClassifier(n_estimators=100, random_state=rs), "GradBoost": GradientBoostingClassifier(random_state=rs)}
    sel = st.multiselect("Models", list(models), default=list(models)[:3], key="ml_m")
    if st.button("🚀 Train models", key="ml_btn") and sel:
        try:
            X = df[feats].copy()
            yy = pd.to_numeric(y, errors="coerce") if task == "regression" else y.astype(str)
            msk = X.notna().all(axis=1) | True
            X, yy = X.loc[yy.notna()], yy.dropna()
            X = X.loc[yy.index]
            if len(X) < 20: st.warning("Very few rows; results may be unstable."); return
            if len(X) > 8000: X, _, yy, _ = train_test_split(X, yy, train_size=8000, random_state=rs)
            Xt, Xte, yt, yte = train_test_split(X, yy, test_size=ts, random_state=rs)
            pre = build_preprocessor(Xt)
            rows: Any = []; best: Any = None; preds: Any = None
            bar = st.progress(0)
            for i, name in enumerate(sel):
                p = Pipeline([("pre", pre), ("m", models[name])])
                p.fit(Xt, yt); pr = p.predict(Xte)
                if task == "regression":
                    mae = mean_absolute_error(yte, pr); mse = mean_squared_error(yte, pr)
                    rows.append({"model": name, "MAE": round(float(mae), 3), "RMSE": round(float(np.sqrt(mse)), 3), "R2": round(float(r2_score(yte, pr)), 3)})
                    key = float(r2_score(yte, pr))
                else:
                    rows.append({"model": name, "Acc": round(float(accuracy_score(yte, pr)), 3), "Prec": round(float(precision_score(yte, pr, average="weighted", zero_division=0)), 3), "Rec": round(float(recall_score(yte, pr, average="weighted", zero_division=0)), 3), "F1": round(float(f1_score(yte, pr, average="weighted", zero_division=0)), 3)})
                    key = float(f1_score(yte, pr, average="weighted", zero_division=0))
                if best is None or key > best[0]: best = (key, name, p, pr)
                bar.progress((i + 1) / len(sel))
            res = pd.DataFrame(rows).sort_values("R2" if task == "regression" else "F1", ascending=False)
            st.dataframe(res, use_container_width=True)
            st.success(f"Best model: **{best[1]}** — business pick for deployment.")
            st.session_state["predictions_df"] = pd.DataFrame({"actual": yte.values[:500], "predicted": (best[3][:500] if task == "regression" else best[3][:500])})
            if HAS_PLOTLY and task == "regression":
                st.plotly_chart(px.scatter(x=yte, y=best[3], labels={"x": "actual", "y": "predicted"}, title="Actual vs Predicted"), use_container_width=True)
            if task == "classification":
                st.write(classification_report(yte, best[3], zero_division=0))
                st.dataframe(pd.DataFrame(confusion_matrix(yte, best[3])), use_container_width=True)
        except Exception as e: st.error(f"Training failed: {e}")
def render_clustering(df, ctypes):
    """K-Means with elbow, silhouette and PCA plot."""
    st.header("🧩 Clustering & Segmentation")
    if not HAS_SKLEARN: st.error("Install scikit-learn."); return
    nums = ctypes["numeric"]
    if len(nums) < 2: st.warning("Need 2+ numeric cols."); return
    feats = st.multiselect("Features", nums, default=nums[:3], key="cl_f")
    k = st.slider("Clusters (k)", 2, 10, 3, key="cl_k")
    if st.button("Run K-Means", key="cl_btn") and len(feats) >= 2:
        try:
            X = df[feats].dropna()
            if len(X) < 10: st.warning("Too few rows."); return
            Xs = StandardScaler().fit_transform(X)
            km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
            lab = km.labels_
            try: sil = silhouette_score(Xs, lab); st.write(f"Silhouette: {sil:.3f} (higher=better separated).")
            except Exception: pass
            prof = pd.DataFrame(Xs, columns=feats); prof["cluster"] = lab
            st.dataframe(prof.groupby("cluster")[feats].mean().round(3), use_container_width=True)
            st.dataframe(pd.Series(lab).value_counts().rename("size").to_frame(), use_container_width=True)
            p2 = PCA(n_components=2).fit_transform(Xs)
            if HAS_PLOTLY:
                st.plotly_chart(px.scatter(x=p2[:, 0], y=p2[:, 1], color=lab.astype(str), title="PCA clusters", labels={"x": "PC1", "y": "PC2", "color": "cluster"}), use_container_width=True)
            inertias = []
            for kk in range(2, min(9, len(X))):
                inertias.append(KMeans(n_clusters=kk, n_init=10, random_state=42).fit(Xs).inertia_)
            if HAS_PLOTLY:
                st.plotly_chart(px.line(x=list(range(2, 2 + len(inertias))), y=inertias, title="Elbow method", labels={"x": "k", "y": "inertia"}), use_container_width=True)
            st.info("Business read: compare cluster means — e.g. high-spend vs low-spend groups for targeting.")
        except Exception as e: st.error(f"Clustering failed: {e}")

def render_forecast(df, ctypes):
    """Trend, moving average and simple forecast."""
    st.header("🔮 Time-Series & Forecasting")
    dts, nums = ctypes["datetime"], ctypes["numeric"]
    if not dts or not nums: st.warning("Need a date + numeric column."); return
    dc = st.selectbox("Date", dts, key="fc_d")
    mc = st.selectbox("Measure", nums, key="fc_m")
    freq = st.selectbox("Aggregate", ["D", "W", "M", "Q", "Y"], index=2, key="fc_f")
    hz = st.slider("Forecast periods", 1, 24, 6, key="fc_h")
    try:
        d = df[[dc, mc]].copy(); d[dc] = pd.to_datetime(d[dc], errors="coerce")
        d = d.dropna().sort_values(dc).set_index(dc).resample(freq)[mc].sum(numeric_only=True)
        d = d.asfreq(freq, fill_value=0)
        if len(d) < 4: st.warning("Too few periods."); return
        ma = d.rolling(min(3, len(d))).mean()
        x = np.arange(len(d)); slope, icept = np.polyfit(x, d.values.astype(float), 1)
        fut_x = np.arange(len(d), len(d) + hz); fc = slope * fut_x + icept
        try: last = d.index[-1]; fi = pd.date_range(last, periods=hz + 1, freq=freq)[1:]
        except Exception: fi = [f"F{i+1}" for i in range(hz)]
        if HAS_PLOTLY:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=d.index, y=d.values, name="History"))
            fig.add_trace(go.Scatter(x=d.index, y=ma.values, name="Moving avg"))
            fig.add_trace(go.Scatter(x=fi, y=fc, name="Forecast", line=dict(dash="dash")))
            fig.update_layout(title=f"{mc} — history vs forecast")
            st.plotly_chart(fig, use_container_width=True)
        st.write(f"Peak: {d.max():,.0f} on {d.idxmax()}; Low: {d.min():,.0f} on {d.idxmin()}. Trend slope {slope:+.1f}/period.")
        st.caption("Limitations: linear-trend forecast ignores seasonality/shocks; use for directional planning only.")
        st.dataframe(pd.DataFrame({"forecast": fc}, index=fi), use_container_width=True)
    except Exception as e: st.error(f"Forecast failed: {e}")
def render_whatif(df, ctypes):
    """Scenario planner with base/optimistic/pessimistic."""
    st.header("🧮 What-If Analysis")
    nums = ctypes["numeric"]
    if not nums: st.warning("No numeric cols."); return
    kpi = st.selectbox("KPI", nums, key="wi_k")
    base = float(pd.to_numeric(df[kpi], errors="coerce").sum())
    st.write(f"Current total **{kpi}**: {base:,.0f}")
    o = st.slider("Optimistic %", 0, 100, 15, key="wi_o")
    p = st.slider("Pessimistic %", -60, 0, -10, key="wi_p")
    c = st.slider("Custom %", -50, 100, 5, key="wi_c")
    sc = pd.DataFrame({"Scenario": ["Pessimistic", "Base", "Custom", "Optimistic"], "Change %": [p, 0, c, o]})
    sc["Projected"] = sc["Change %"].apply(lambda x: base * (1 + x / 100))
    sc["Impact"] = sc["Projected"] - base
    st.dataframe(sc.round(1), use_container_width=True)
    if HAS_PLOTLY:
        st.plotly_chart(px.bar(sc, x="Scenario", y="Projected", title="Scenario comparison"), use_container_width=True)
    st.download_button("⬇️ Download scenarios (CSV)", sc.to_csv(index=False).encode(), "scenarios.csv", "text/csv", key="wi_dl")

def generate_automated_insights(df, ctypes):
    """Rule-based insights with real values."""
    ins = []
    try:
        miss = df.isna().sum(); mp = (df.isna().mean() * 100).round(1)
        if miss.sum() > 0:
            c = miss.idxmax(); ins.append(f"Missing-data risk: {c} has {miss[c]:,} missing ({mp[c]}%). Fix source capture.")
        else: ins.append("Missing-data check: no missing cells. Maintain validation.")
        dup = int(df.duplicated().sum())
        ins.append(f"Duplicate risk: {dup:,} rows ({dup/max(len(df),1)*100:.1f}%).")
        if len(ctypes["numeric"]) >= 2:
            corr = df[ctypes["numeric"]].corr(numeric_only=True)
            bv, bp = 0, None
            for i in range(len(corr.columns)):
                for j in range(i + 1, len(corr.columns)):
                    v = corr.iloc[i, j]
                    if pd.notna(v) and abs(v) > abs(bv): bv, bp = v, (corr.columns[i], corr.columns[j])
            if bp: ins.append(f"Strongest correlation: {bp[0]} - {bp[1]} (r={bv:.2f}). Correlation is not causation.")
        for n in ctypes["numeric"][:3]:
            s = pd.to_numeric(df[n], errors="coerce").dropna()
            if len(s) > 10:
                q1, q3 = s.quantile(.25), s.quantile(.75); iqr = q3 - q1 or 1
                oc = int(((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr)).sum())
                ins.append(f"Outliers in {n}: {oc} rows ({oc/len(s)*100:.1f}% via IQR).")
        if ctypes["categorical"] and ctypes["numeric"]:
            cat, m = ctypes["categorical"][0], ctypes["numeric"][0]
            g = df.groupby(cat)[m].sum(numeric_only=True).sort_values(ascending=False)
            if len(g):
                ins.append(f"Top contributor: {g.index[0]} = {g.iloc[0]:,.0f} ({g.iloc[0]/g.sum()*100:.1f}% of {m}).")
                ins.append(f"Bottom contributor: {g.index[-1]} = {g.iloc[-1]:,.0f}. Needs attention.")
                hhi = float((((g / g.sum())) ** 2).sum())
                ins.append(f"Concentration HHI={hhi:.3f} ({'high risk' if hhi > .25 else 'ok'}).")
        if ctypes["datetime"] and ctypes["numeric"]:
            dc, m = ctypes["datetime"][0], ctypes["numeric"][0]
            t = df.assign(_d=pd.to_datetime(df[dc], errors="coerce")).dropna(subset=["_d"]).sort_values("_d").set_index("_d").resample("M")[m].sum(numeric_only=True)
            if len(t) >= 3:
                ch = t.pct_change().dropna() * 100
                ins.append(f"Fastest growth: {ch.idxmax().date()} ({ch.max():+.1f}% MoM).")
                ins.append(f"Largest decline: {ch.idxmin().date()} ({ch.min():+.1f}% MoM).")
                ins.append(f"Volatility CV={t.std()/abs(t.mean())*100:.1f}% for {m}.")
        while len(ins) < 8:
            ins.append(f"Shape: {len(df):,} rows x {df.shape[1]} cols.")
    except Exception as e:
        ins.append(f"Insight note: {e}")
    return ins[:12]
def render_downloads(df):
    """Download center plus in-memory HTML report."""
    st.header("📥 Report & Download Center")
    from datetime import datetime as _dt
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("⬇️ Cleaned CSV", df.to_csv(index=False).encode(), "cleaned_data.csv", "text/csv", key="dl_clean")
        dq = pd.DataFrame({"missing": df.isna().sum(), "missing_pct": (df.isna().mean() * 100).round(2), "unique": df.nunique()})
        st.download_button("⬇️ Data-quality CSV", dq.to_csv().encode(), "data_quality.csv", "text/csv", key="dl_dq")
        summ = f"InsightForge summary\nRows: {len(df)}\nCols: {list(df.columns)}\nInsights:\n" + "\n".join(st.session_state.get("insights_list") or [])
        st.download_button("⬇️ Summary TXT", summ.encode(), "summary.txt", "text/plain", key="dl_sum")
    with c2:
        st.download_button("⬇️ Filtered CSV", df.to_csv(index=False).encode(), "filtered_data.csv", "text/csv", key="dl_filt")
        if st.session_state.get("predictions_df") is not None:
            st.download_button("⬇️ Predictions CSV", st.session_state["predictions_df"].to_csv(index=False).encode(), "predictions.csv", "text/csv", key="dl_pred")
        else: st.info("Train ML to enable predictions download.")
        bi = "\n".join(st.session_state.get("insights_list") or ["Run Business module first."])
        st.download_button("⬇️ Insights TXT", bi.encode(), "insights.txt", "text/plain", key="dl_ins")
    html = f"<html><head><title>InsightForge Report</title></head><body><h1>InsightForge AI Report</h1><p>Generated {_dt.now():%Y-%m-%d %H:%M}</p><p>Rows {len(df)}, Cols {df.shape[1]}</p><ul>" + "".join(f"<li>{x}</li>" for x in (st.session_state.get('insights_list') or [])) + "</ul>" + df.head(20).to_html() + f"<p>{APP_FOOTER}</p></body></html>"
    st.download_button("⬇️ HTML report", html.encode(), "insightforge_report.html", "text/html", key="dl_html")

def render_about():
    """Portfolio about page."""
    st.header("ℹ️ About")
    st.markdown("**InsightForge AI** — portfolio data-science & business-analytics platform by **Bhaskar Kewalramani**.")
    st.markdown("Features: profiling, cleaning, EDA (15 charts), business/Pareto/ABC, KPI dashboard, stats, ML (11 models), clustering, forecasting, what-if, insights, downloads.")
    st.markdown("**Stack:** Streamlit, pandas, numpy, plotly, matplotlib, seaborn, scikit-learn, scipy, openpyxl. No API key, no paid services.")
    st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")
    st.markdown("**Deploy (Community Cloud):** push app.py + requirements.txt to GitHub → share.streamlit.io → New app → select repo/branch/app.py → Deploy.")
    st.markdown("GitHub placeholder: `https://github.com/<your-username>/insightforge-ai`")
    st.markdown(f"<div class='footer'>{APP_FOOTER}</div>", unsafe_allow_html=True)
def main():
    """Sidebar navigation, uploads, filters and routing."""
    st.sidebar.title("🔷 InsightForge AI")
    st.sidebar.caption("Data Science & Business Analytics Platform")
    page = st.sidebar.radio("Navigation", ["🏠 Home", "📤 Data Profile", "🧹 Cleaning", "📊 EDA", "💼 Business", "📌 KPIs", "📈 Statistics", "🤖 ML", "🧩 Clustering", "🔮 Forecast", "🧮 What-If", "💡 Insights", "📥 Reports", "ℹ️ About"], key="nav")
    st.sidebar.divider()
    st.sidebar.subheader("📁 Data")
    up = st.sidebar.file_uploader("Upload CSV/Excel", type=["csv", "xlsx", "xls"], key="upl")
    if up is not None:
        try:
            raw = up.getvalue()
            df = load_data(raw, up.name)
            st.session_state["original_df"] = df; st.session_state["cleaned_df"] = df.copy()
            st.session_state["filtered_df"] = None; st.session_state["file_name"] = up.name
            st.session_state["file_size"] = len(raw); st.session_state["clean_log"] = [f"Loaded {up.name} ({len(df)} rows)."]
            st.sidebar.success(f"Loaded {len(df):,} rows.")
        except Exception as e: st.sidebar.error(f"Upload failed: {e}")
    if st.sidebar.button("🎲 Load sample data", key="sample_btn"):
        df = generate_sample_data()
        st.session_state["original_df"] = df; st.session_state["cleaned_df"] = df.copy()
        st.session_state["filtered_df"] = None; st.session_state["file_name"] = "synthetic_demo.csv"
        st.session_state["file_size"] = int(df.memory_usage(deep=True).sum())
        st.session_state["clean_log"] = ["Loaded SYNTHETIC demo dataset (clearly labelled)."]
        st.sidebar.success("Synthetic demo loaded (labelled).")
    pal = st.sidebar.selectbox("Chart theme", list(PALETTES), key="pal")
    base = st.session_state.get("cleaned_df") if st.session_state.get("cleaned_df") is not None else st.session_state.get("original_df")
    if base is not None and len(base):
        st.sidebar.subheader("🔎 Filters")
        fdf = base.copy()
        for c in base.select_dtypes(include="object").columns[:4]:
            vals = sorted([str(v) for v in base[c].dropna().unique()])[:50]
            pick = st.sidebar.multiselect(c, vals, key=f"flt_{c}")
            if pick: fdf = fdf[fdf[c].astype(str).isin(pick)]
        for c in base.select_dtypes(include=np.number).columns[:2]:
            lo, hi = float(base[c].min()), float(base[c].max())
            if lo < hi:
                r = st.sidebar.slider(c, lo, hi, (lo, hi), key=f"rng_{c}")
                fdf = fdf[(fdf[c] >= r[0]) & (fdf[c] <= r[1])]
        st.session_state["filtered_df"] = fdf
        st.sidebar.caption(f"Filtered: {len(fdf):,} / {len(base):,} rows.")
        with st.sidebar.expander("ℹ️ Dataset info"):
            st.write(f"File: {st.session_state.get('file_name')}")
            st.write(f"Rows: {len(fdf):,}, Cols: {fdf.shape[1]}")
            st.write(f"Missing: {int(fdf.isna().sum().sum()):,}")
    if st.sidebar.button("♻️ Reset app", key="reset_btn"):
        for k in ["original_df", "cleaned_df", "filtered_df", "predictions_df"]:
            st.session_state[k] = None
        st.session_state["clean_log"] = []; st.session_state["insights_list"] = []
        st.rerun()
    df = get_active_df()
    if page == "🏠 Home":
        render_home(); return
    if page == "ℹ️ About":
        render_about(); return
    if df is None or len(df) == 0:
        render_home()
        st.warning("No data yet — upload a file or load sample data from the sidebar.")
        return
    ct = detect_column_types(df)
    if getattr(df, "attrs", {}).get("synthetic"):
        st.caption("Synthetic demonstration data.")
    elif (st.session_state.get("file_name") or "") == "synthetic_demo.csv":
        st.info("You are viewing SYNTHETIC demo data (labelled). Upload real data for true analysis.")
    if page == "📤 Data Profile": render_data_profile(df, ct)
    elif page == "🧹 Cleaning": render_cleaning(st.session_state.get("original_df") if st.session_state.get("original_df") is not None else df, ct)
    elif page == "📊 EDA": render_eda(df, ct, pal)
    elif page == "💼 Business": render_business(df, ct)
    elif page == "📌 KPIs": render_kpi_dashboard(df, ct)
    elif page == "📈 Statistics": render_statistics(df, ct)
    elif page == "🤖 ML": render_ml(df, ct)
    elif page == "🧩 Clustering": render_clustering(df, ct)
    elif page == "🔮 Forecast": render_forecast(df, ct)
    elif page == "🧮 What-If": render_whatif(df, ct)
    elif page == "💡 Insights":
        st.header("💡 Automated Insights")
        ins = generate_automated_insights(df, ct)
        for i, x in enumerate(ins, 1): st.markdown(f"**{i}.** {x}")
        st.session_state["insights_list"] = ins
    elif page == "📥 Reports": render_downloads(df)
    st.markdown(f"<div class='footer'>{APP_FOOTER}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
