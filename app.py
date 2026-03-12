import streamlit as st
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Iris Predictor",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    :root {
        --sky-50:  #f0f9ff;
        --sky-100: #e0f2fe;
        --sky-200: #bae6fd;
        --sky-500: #0ea5e9;
        --sky-600: #0284c7;
        --sky-700: #0369a1;
        --slate-50:  #f8fafc;
        --slate-700: #334155;
        --white: #ffffff;
    }
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: var(--sky-50) !important;
        color: var(--slate-700);
    }
    .main .block-container {
        padding: 2rem 2.5rem 3rem;
        max-width: 1280px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, var(--white) 0%, var(--sky-100) 100%);
        border-right: 1px solid var(--sky-200);
    }
    .hero {
        background: linear-gradient(135deg, var(--sky-500) 0%, var(--sky-700) 100%);
        border-radius: 20px;
        padding: 2rem 2.4rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(14,165,233,0.15);
    }
    .hero h1 { margin:0; font-size:2rem; font-weight:700; letter-spacing:-0.02em; }
    .hero p  { margin:0.4rem 0 0; font-size:1rem; opacity:0.9; }

    /* Custom button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669);
        color: var(--white);
        border: none;
        border-radius: 12px;
        padding: 0.55rem 1.6rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669, #047857);
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── ML Model ─────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    """Load pre-trained model if available, else fallback to training."""
    iris = load_iris()
    model_path = "model.joblib"
    
    if os.path.exists(model_path):
        clf = joblib.load(model_path)
    else:
        clf = RandomForestClassifier(random_state=42, n_estimators=50)
        clf.fit(iris.data, iris.target)
        
    return clf, iris.target_names

clf, target_names = get_model()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding-bottom:1rem;">
            <div style="font-size:2.2rem;">🌸</div>
            <div style="font-size:1.15rem; font-weight:700; color:#0369a1;">Iris Predictor</div>
            <div style="font-size:0.75rem; color:#64748b; margin-top:2px;">Antigravity Analytics Suite</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("**📂 Upload Iris Dataset**")
    uploaded_file = st.file_uploader(
        "Drop a CSV file here",
        type=["csv"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        st.success(f"✅ `{uploaded_file.name}`")
    st.markdown("---")

# ── Main Content ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>🌸 Iris Species Predictor</h1>
        <p>Upload a CSV file containing flower measurements (sepal & petal dimensions) to automatically predict their species.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if uploaded_file is None:
    st.info("👈 Please upload a **.csv** file from the sidebar to predict Iris species.")
    st.stop()

# ── Data Processing ────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)

with st.spinner("🧠 Analyzing and predicting…"):
    df = load_csv(uploaded_file)
    
    # Isolate numeric columns for inference (expecting at least 4 for Iris predictions)
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    if len(numeric_cols) < 4:
        st.error(f"⚠️ Error: The model requires 4 numeric features (Sepal Length, Sepal Width, Petal Length, Petal Width). Only found {len(numeric_cols)} in your dataset.")
        st.dataframe(df.head())
        st.stop()
    
    # Use the first 4 numeric columns as features
    # (assuming order mostly matches standard sepal length, width, petal length, width)
    # We drop any NaNs so the model doesn't crash during inference!
    if df[numeric_cols[:4]].isnull().any().any():
        st.warning("Found null values in your numeric features. We are predicting on complete rows only.")
        df = df.dropna(subset=numeric_cols[:4]).reset_index(drop=True)

    X = df[numeric_cols[:4]].values
    predictions = clf.predict(X)
    
    # Map predictions to string names provided by Scikit-Learn
    df["Predicted Species"] = [target_names[p] for p in predictions]

# ── Results Layout ─────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 📋 Prediction Results")
    st.caption("Here is your dataset with the newly appended **Predicted Species** column at the far right.")
    st.dataframe(
        df,
        use_container_width=True,
        height=500
    )

with col2:
    st.markdown("### � Summary")
    species_counts = df["Predicted Species"].value_counts().reset_index()
    species_counts.columns = ["Species", "Count"]
    st.dataframe(species_counts, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📥 Export")
    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Predictions",
        data=csv_bytes,
        file_name="iris_predictions.csv",
        mime="text/csv",
        use_container_width=True
    )
