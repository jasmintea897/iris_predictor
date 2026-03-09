import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import io
import zipfile
import base64
from datetime import datetime

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataLens · Antigravity",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — Airy / Light-Blue Palette ───────────────────────────────────
st.markdown(
    """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Root palette */
    :root {
        --sky-50:  #f0f9ff;
        --sky-100: #e0f2fe;
        --sky-200: #bae6fd;
        --sky-400: #38bdf8;
        --sky-500: #0ea5e9;
        --sky-600: #0284c7;
        --sky-700: #0369a1;
        --slate-50:  #f8fafc;
        --slate-100: #f1f5f9;
        --slate-200: #e2e8f0;
        --slate-500: #64748b;
        --slate-700: #334155;
        --slate-900: #0f172a;
        --white: #ffffff;
    }

    /* Global */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--sky-50) !important;
        color: var(--slate-700);
    }

    /* Main container */
    .main .block-container {
        padding: 2rem 2.5rem 3rem;
        max-width: 1280px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, var(--white) 0%, var(--sky-100) 100%);
        border-right: 1px solid var(--sky-200);
    }
    [data-testid="stSidebar"] .block-container {
        padding: 1.5rem 1.2rem;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: var(--white);
        border: 1px solid var(--sky-200);
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 12px rgba(14,165,233,0.07);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        box-shadow: 0 6px 24px rgba(14,165,233,0.14);
        transform: translateY(-2px);
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--sky-600);
    }
    [data-testid="stMetricValue"] {
        font-size: 1.7rem;
        font-weight: 700;
        color: var(--slate-900);
    }

    /* Rounded card wrapper used via st.container */
    .card {
        background: var(--white);
        border: 1px solid var(--sky-200);
        border-radius: 20px;
        padding: 1.6rem 1.8rem;
        box-shadow: 0 4px 20px rgba(14,165,233,0.08);
        margin-bottom: 1.5rem;
    }

    /* Section headings */
    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--sky-700);
        margin-bottom: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }

    /* Styled data-type badge */
    .dtype-badge {
        display: inline-block;
        background: var(--sky-100);
        color: var(--sky-700);
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    /* Null-count pill */
    .null-pill-ok  { background:#dcfce7; color:#166534; border-radius:999px; padding:2px 10px; font-size:0.72rem; font-weight:600; }
    .null-pill-bad { background:#fee2e2; color:#991b1b; border-radius:999px; padding:2px 10px; font-size:0.72rem; font-weight:600; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--sky-500), var(--sky-600));
        color: var(--white);
        border: none;
        border-radius: 12px;
        padding: 0.55rem 1.6rem;
        font-weight: 600;
        font-size: 0.88rem;
        letter-spacing: 0.03em;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 3px 12px rgba(14,165,233,0.30);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--sky-600), var(--sky-700));
        box-shadow: 0 6px 18px rgba(14,165,233,0.40);
        transform: translateY(-1px);
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: var(--white);
        border: none;
        border-radius: 12px;
        padding: 0.55rem 1.6rem;
        font-weight: 600;
<<<<<<< HEAD
=======
        font-size: 0.88rem;
        box-shadow: 0 3px 12px rgba(16,185,129,0.30);
>>>>>>> a3a3ac2 (Initial commit: DataLens Streamlit app)
        transition: all 0.2s ease;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669, #047857);
<<<<<<< HEAD
        transform: translateY(-1px);
    }
=======
        box-shadow: 0 6px 18px rgba(16,185,129,0.40);
        transform: translateY(-1px);
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        border-radius: 10px;
        border: 1px solid var(--sky-200);
        background: var(--white);
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed var(--sky-300, #7dd3fc);
        border-radius: 14px;
        background: var(--sky-50);
        padding: 0.5rem;
        transition: border-color 0.2s;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--sky-500);
    }

    /* Divider */
    hr { border-color: var(--sky-200); }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--sky-200);
    }

    /* Hero header */
    .hero {
        background: linear-gradient(135deg, var(--sky-500) 0%, var(--sky-700) 100%);
        border-radius: 24px;
        padding: 2rem 2.4rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(14,165,233,0.25);
    }
    .hero h1 { margin:0; font-size:2rem; font-weight:700; letter-spacing:-0.02em; }
    .hero p  { margin:0.4rem 0 0; font-size:1rem; opacity:0.88; }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 4rem 2rem;
        color: var(--slate-500);
    }
    .empty-state .icon { font-size: 4rem; margin-bottom: 1rem; }
    .empty-state h3 { font-size: 1.2rem; font-weight: 600; color: var(--slate-700); margin-bottom: 0.5rem; }
    .empty-state p  { font-size: 0.9rem; }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--sky-100);
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 9px;
        font-weight: 500;
        font-size: 0.88rem;
    }
    .stTabs [aria-selected="true"] {
        background: var(--white) !important;
        color: var(--sky-600) !important;
        box-shadow: 0 2px 8px rgba(14,165,233,0.15);
    }
>>>>>>> a3a3ac2 (Initial commit: DataLens Streamlit app)
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Helpers ──────────────────────────────────────────────────────────────────

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with rows containing any null values dropped."""
    return df.dropna()


def plot_scatter(df: pd.DataFrame, x_col: str, y_col: str, color_col=None) -> px.scatter:
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col if color_col and color_col != "None" else None,
        title=f"{y_col}  ↔  {x_col}",
        template="plotly_white",
        color_continuous_scale="Blues",
        hover_data=df.columns.tolist(),
    )
    fig.update_traces(
        marker=dict(size=8, opacity=0.78, line=dict(width=0.6, color="white")),
    )
    fig.update_layout(
        font_family="Inter, sans-serif",
        title_font_size=17,
        title_font_color="#0369a1",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(240,249,255,0.6)",
        xaxis=dict(gridcolor="#bae6fd", gridwidth=1, zeroline=False),
        yaxis=dict(gridcolor="#bae6fd", gridwidth=1, zeroline=False),
        margin=dict(l=40, r=20, t=55, b=40),
        legend=dict(bgcolor="rgba(255,255,255,0.85)", bordercolor="#bae6fd", borderwidth=1),
    )
    return fig


def build_zip(fig, df_clean: pd.DataFrame) -> bytes:
    """Bundle the chart HTML and cleaned CSV into a ZIP archive."""
    chart_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    csv_bytes = df_clean.to_csv(index=False).encode("utf-8")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        zf.writestr(f"scatter_chart_{ts}.html", chart_html)
        zf.writestr(f"cleaned_data_{ts}.csv", csv_bytes)
    return buf.getvalue()


def null_summary(df: pd.DataFrame) -> pd.DataFrame:
    null_counts = df.isnull().sum()
    null_pct    = (null_counts / len(df) * 100).round(2)
    return pd.DataFrame({
        "Column":      df.columns,
        "Data Type":   [str(dt) for dt in df.dtypes],
        "Null Count":  null_counts.values,
        "Null %":      null_pct.values,
    }).reset_index(drop=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding-bottom:1rem;">
            <div style="font-size:2.2rem;">🔭</div>
            <div style="font-size:1.15rem; font-weight:700; color:#0369a1;">DataLens</div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:2px;">Antigravity Analytics Suite</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("**📂 Upload Dataset**")
    uploaded_file = st.file_uploader(
        label="Drop a CSV file here",
        type=["csv"],
        help="Only .csv files are accepted.",
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.success(f"✅ `{uploaded_file.name}`")
        st.caption(f"Size: {uploaded_file.size / 1024:.1f} KB")

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:0.75rem; color:#94a3b8; text-align:center;">
        Antigravity DataLens v1.0<br/>
        <span style="color:#bae6fd">●</span> Ready
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Main Content ───────────────────────────────────────────────────────────────

# Hero Header
st.markdown(
    """
    <div class="hero">
        <h1>🔭 DataLens · Antigravity</h1>
        <p>Upload a CSV file to explore, profile, and visualize your dataset instantly.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.markdown(
        """
        <div class="empty-state">
            <div class="icon">📤</div>
            <h3>No file uploaded yet</h3>
            <p>Use the sidebar on the left to upload a <strong>.csv</strong> file and get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)

with st.spinner("📊 Loading your dataset…"):
    df = load_csv(uploaded_file)

df_clean = clean_dataframe(df)
numeric_cols  = df.select_dtypes(include="number").columns.tolist()
categoric_cols = df.select_dtypes(exclude="number").columns.tolist()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab_health, tab_viz, tab_data = st.tabs([
    "🩺 Data Health",
    "📈 Scatter Explorer",
    "📋 Raw Data",
])

# ╔══════════════════════════════╗
# ║      TAB 1 — DATA HEALTH    ║
# ╚══════════════════════════════╝
with tab_health:
    # KPI row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("🗂 Total Rows",    f"{len(df):,}")
    kpi2.metric("🏛 Columns",       f"{df.shape[1]:,}")
    kpi3.metric("🔢 Numeric Cols",  f"{len(numeric_cols):,}")
    kpi4.metric("⚠️ Rows w/ Nulls", f"{df.isnull().any(axis=1).sum():,}")

    st.markdown("<br/>", unsafe_allow_html=True)

    # Column profile table
    st.markdown(
        '<div class="section-title">🏷️ Column Profile</div>',
        unsafe_allow_html=True,
    )

    summary_df = null_summary(df)

    # Render a pretty styled table
    def fmt_row(row):
        dtype_badge = f'<span class="dtype-badge">{row["Data Type"]}</span>'
        null_count  = int(row["Null Count"])
        null_pill   = (
            f'<span class="null-pill-ok">✓ {null_count}</span>'
            if null_count == 0
            else f'<span class="null-pill-bad">✗ {null_count} ({row["Null %"]}%)</span>'
        )
        return dtype_badge, null_pill

    header_html = (
        '<table style="width:100%; border-collapse:collapse; font-size:0.88rem;">'
        '<thead>'
        '<tr style="background:#e0f2fe; color:#0369a1;">'
        '<th style="padding:10px 14px; border-radius:8px 0 0 8px; text-align:left;">#</th>'
        '<th style="padding:10px 14px; text-align:left;">Column Name</th>'
        '<th style="padding:10px 14px; text-align:left;">Data Type</th>'
        '<th style="padding:10px 14px; border-radius:0 8px 8px 0; text-align:left;">Null Values</th>'
        '</tr>'
        '</thead>'
        '<tbody>'
    )
    rows_html = ""
    for i, row in summary_df.iterrows():
        dtype_badge, null_pill = fmt_row(row)
        bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
        rows_html += (
            f'<tr style="background:{bg}; border-bottom:1px solid #e0f2fe;">'
            f'<td style="padding:9px 14px; color:#94a3b8;">{i+1}</td>'
            f'<td style="padding:9px 14px; font-weight:600; color:#334155;">{row["Column"]}</td>'
            f'<td style="padding:9px 14px;">{dtype_badge}</td>'
            f'<td style="padding:9px 14px;">{null_pill}</td>'
            '</tr>'
        )
    footer_html = "</tbody></table>"

    st.markdown(
        f'<div class="card">{header_html}{rows_html}{footer_html}</div>',
        unsafe_allow_html=True,
    )

    # Null heatmap bar chart
    null_counts = summary_df[summary_df["Null Count"] > 0]
    if not null_counts.empty:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">📊 Null Value Distribution</div>',
            unsafe_allow_html=True,
        )
        fig_null = px.bar(
            null_counts,
            x="Column",
            y="Null Count",
            color="Null %",
            color_continuous_scale="Blues",
            template="plotly_white",
            text="Null Count",
        )
        fig_null.update_traces(textposition="outside", marker_line_width=0)
        fig_null.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(240,249,255,0.6)",
            xaxis=dict(gridcolor="#bae6fd"),
            yaxis=dict(gridcolor="#bae6fd"),
            margin=dict(l=30, r=20, t=20, b=30),
            coloraxis_colorbar=dict(title="Null %"),
        )
        st.plotly_chart(fig_null, use_container_width=True)
    else:
        st.success("🎉 **Zero null values found!** Your dataset is complete.")

    # Numeric summary stats
    if numeric_cols:
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">📐 Descriptive Statistics (Numeric)</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(
            df[numeric_cols].describe().T.round(3),
            use_container_width=True,
        )


# ╔══════════════════════════════════╗
# ║    TAB 2 — SCATTER EXPLORER     ║
# ╚══════════════════════════════════╝
with tab_viz:
    if len(numeric_cols) < 2:
        st.warning("⚠️ At least **2 numeric columns** are required for a scatter plot.")
    else:
        st.markdown(
            '<div class="section-title">⚙️ Configure Chart</div>',
            unsafe_allow_html=True,
        )

        ctrl_left, ctrl_mid, ctrl_right = st.columns([1, 1, 1])
        with ctrl_left:
            x_col = st.selectbox("X-Axis", options=numeric_cols, index=0, key="x_col")
        with ctrl_mid:
            y_col = st.selectbox(
                "Y-Axis",
                options=numeric_cols,
                index=min(1, len(numeric_cols) - 1),
                key="y_col",
            )
        with ctrl_right:
            color_options = ["None"] + categoric_cols + numeric_cols
            color_col = st.selectbox("Color By (optional)", options=color_options, key="color_col")

        st.markdown("<br/>", unsafe_allow_html=True)

        if x_col == y_col:
            st.info("ℹ️ Select two **different** columns for X and Y axes.")
        else:
            fig_scatter = plot_scatter(
                df,
                x_col,
                y_col,
                color_col if color_col != "None" else None,
            )

            st.plotly_chart(fig_scatter, use_container_width=True, key="scatter")

            st.markdown("---")
            st.markdown(
                '<div class="section-title">📥 Download Report</div>',
                unsafe_allow_html=True,
            )
            st.caption(
                "Downloads a **ZIP** file containing the interactive chart (`.html`) "
                "and the cleaned dataset (rows with nulls removed, `.csv`)."
            )

            col_dl1, col_dl2, _ = st.columns([1, 1, 2])

            # ── Chart HTML download
            chart_html_bytes = pio.to_html(
                fig_scatter, full_html=True, include_plotlyjs="cdn"
            ).encode("utf-8")
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")

            with col_dl1:
                st.download_button(
                    label="📊 Download Chart (.html)",
                    data=chart_html_bytes,
                    file_name=f"scatter_chart_{ts}.html",
                    mime="text/html",
                    key="dl_chart",
                )

            # ── Cleaned CSV download
            csv_bytes = df_clean.to_csv(index=False).encode("utf-8")
            with col_dl2:
                st.download_button(
                    label="🗂 Download Cleaned CSV",
                    data=csv_bytes,
                    file_name=f"cleaned_data_{ts}.csv",
                    mime="text/csv",
                    key="dl_csv",
                )

            # ── ZIP bundle
            zip_bytes = build_zip(fig_scatter, df_clean)
            st.download_button(
                label="📦 Download Full Report (.zip)",
                data=zip_bytes,
                file_name=f"datalens_report_{ts}.zip",
                mime="application/zip",
                key="dl_zip",
            )

            # Correlation hint
            with st.expander("📐 Pearson Correlation"):
                corr = df[[x_col, y_col]].corr().iloc[0, 1]
                sign = "positive" if corr > 0 else "negative"
                strength = (
                    "strong" if abs(corr) > 0.7
                    else "moderate" if abs(corr) > 0.4
                    else "weak"
                )
                st.metric(
                    label=f"r({x_col}, {y_col})",
                    value=f"{corr:.4f}",
                    delta=f"{strength} {sign} correlation",
                )


# ╔══════════════════════════════╗
# ║      TAB 3 — RAW DATA       ║
# ╚══════════════════════════════╝
with tab_data:
    search = st.text_input("🔍 Filter rows (searches all columns)", placeholder="Type to search…")
    if search:
        mask = df.apply(lambda col: col.astype(str).str.contains(search, case=False, na=False))
        df_view = df[mask.any(axis=1)]
    else:
        df_view = df

    st.caption(f"Showing **{len(df_view):,}** of **{len(df):,}** rows")
    st.dataframe(df_view, use_container_width=True, height=480)

    csv_raw = df_view.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Filtered View (.csv)",
        data=csv_raw,
        file_name=f"filtered_view_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        key="dl_raw",
    )
