import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from PIL import Image

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Instagram Fake Account Detector",
    page_icon="📸",
    layout="wide"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=JetBrains+Mono:wght@300;400;500&display=swap');

  /* ── Global White Background + Red Text ── */
  html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #ffffff !important;
    color: #cc0000 !important;
  }

  .stApp {
    background-color: #ffffff !important;
  }

  /* Hide Streamlit chrome */
  #MainMenu, footer, header { visibility: hidden; }

  /* Page wrapper */
  .block-container {
    padding: 2.5rem 3rem 4rem;
    max-width: 1100px;
    background-color: #ffffff !important;
  }

  /* ── Hero ── */
  .hero {
    background: #ffffff;
    border: 1.5px solid rgba(204, 0, 0, 0.25);
    border-radius: 6px;
    padding: 2.4rem 2.8rem 2rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 30px rgba(204,0,0,0.07);
  }
  .hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #cc0000, #ff4444, #cc0000);
  }
  .hero::after {
    content: 'DETECTOR';
    position: absolute;
    right: 2rem;
    top: 50%;
    transform: translateY(-50%);
    font-family: 'Bebas Neue', sans-serif;
    font-size: 6rem;
    color: rgba(204,0,0,0.05);
    letter-spacing: 0.15em;
    pointer-events: none;
  }

  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    font-weight: 400;
    letter-spacing: 0.08em;
    color: #cc0000;
    margin: 0 0 0.4rem;
    line-height: 1;
  }
  .hero-sub {
    color: rgba(204, 0, 0, 0.55);
    font-size: 0.88rem;
    font-weight: 400;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
  }
  .accuracy-badge {
    display: inline-block;
    margin-top: 1.2rem;
    background: rgba(204,0,0,0.06);
    border: 1px solid rgba(204,0,0,0.35);
    border-radius: 3px;
    padding: 0.3rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 500;
    color: #cc0000;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }

  /* ── Section headers ── */
  .section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: #cc0000;
    margin: 2.5rem 0 1.2rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.8rem;
  }
  .section-title::before {
    content: '//';
    color: #ff2222;
    font-size: 0.85rem;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(204,0,0,0.3), transparent);
  }

  /* ── Input fields ── */
  .stTextInput > div > div {
    background: #fff5f5 !important;
    border: 1px solid rgba(204,0,0,0.2) !important;
    border-radius: 4px !important;
    color: #cc0000 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .stTextInput > div > div:focus-within {
    border-color: rgba(204,0,0,0.6) !important;
    box-shadow: 0 0 0 3px rgba(204,0,0,0.08) !important;
  }
  .stTextInput input {
    color: #cc0000 !important;
    caret-color: #cc0000;
    background: transparent !important;
  }
  .stTextInput label {
    color: rgba(204, 0, 0, 0.7) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace !important;
  }

  /* ── Detect button ── */
  div.stButton > button {
    background: #cc0000 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.7rem 2.2rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
    box-shadow: 0 4px 15px rgba(204,0,0,0.3);
  }
  div.stButton > button:hover {
    background: #aa0000 !important;
    box-shadow: 0 6px 20px rgba(204,0,0,0.4) !important;
    transform: translateY(-1px);
  }

  /* ── Alert / Result boxes ── */
  .stAlert {
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em;
  }

  /* ── Divider ── */
  hr {
    border: none !important;
    border-top: 1px solid rgba(204,0,0,0.12) !important;
    margin: 2.5rem 0 !important;
  }

  /* ── File uploader ── */
  .stFileUploader {
    background: #fff5f5 !important;
    border: 1px dashed rgba(204,0,0,0.25) !important;
    border-radius: 4px !important;
    padding: 1rem !important;
  }
  .stFileUploader label {
    color: rgba(204,0,0,0.65) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }

  /* ── Dataframe ── */
  .stDataFrame {
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid rgba(204,0,0,0.15) !important;
  }

  /* ── Download button ── */
  div.stDownloadButton > button {
    background: #fff5f5 !important;
    color: #cc0000 !important;
    border: 1px solid rgba(204,0,0,0.3) !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    transition: all 0.2s;
  }
  div.stDownloadButton > button:hover {
    background: rgba(204,0,0,0.08) !important;
    border-color: rgba(204,0,0,0.5) !important;
  }

  /* ── Warning text ── */
  .stWarning {
    background: #fff8f0 !important;
    color: #cc4400 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
  }

  /* ── Paragraph / markdown text ── */
  p, span, div, label {
    color: #cc0000;
  }

  /* ── Column gap fix ── */
  [data-testid="column"] {
    background: transparent !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Load Model ─────────────────────────────────────────────────────────────────
model = joblib.load("instagram_fake_detector.pkl")

# ── Hero Banner ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-title">📸 Instagram Fake Account Detector</p>
  <p class="hero-sub">Paste account metrics below and instantly find out if an account is genuine</p>
  <span class="accuracy-badge">⚡ Model Accuracy — 96%</span>
</div>
""", unsafe_allow_html=True)

# ── Single Account ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Single Account Prediction</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

def typed_number(label, key, col):
    """Text input that accepts typed numbers; returns float."""
    val = col.text_input(label, value="0", key=key)
    try:
        return float(val)
    except ValueError:
        col.warning(f"Enter a valid number for '{label}'")
        return 0.0

with col1:
    profile_pic        = typed_number("Profile Pic (0 = No, 1 = Yes)",     "profile_pic",        col1)
    username_num       = typed_number("Nums / Length Username",              "username_num",        col1)
    fullname_words     = typed_number("Fullname Word Count",                 "fullname_words",      col1)
    fullname_num       = typed_number("Nums / Length Fullname",              "fullname_num",        col1)
    name_username      = typed_number("Name == Username (0 / 1)",            "name_username",       col1)

with col2:
    description_length = typed_number("Bio / Description Length",            "description_length",  col2)
    external_url       = typed_number("External URL (0 = No, 1 = Yes)",      "external_url",        col2)
    private            = typed_number("Private Account (0 = No, 1 = Yes)",   "private",             col2)
    posts              = typed_number("Number of Posts",                     "posts",               col2)
    followers          = typed_number("Followers Count",                     "followers",           col2)
    follows            = typed_number("Following Count",                     "follows",             col2)

st.write("")
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    detect = st.button("🔍 Run Detection")

if detect:
    data = [[
        profile_pic, username_num, fullname_words, fullname_num,
        name_username, description_length, external_url, private,
        posts, followers, follows
    ]]

    prediction  = model.predict(data)[0]
    probability = model.predict_proba(data)[0]
    fake_prob   = round(probability[1] * 100, 2)
    real_prob   = round(probability[0] * 100, 2)

    st.write("")
    if prediction == 1:
        st.error(f"⚠️  Fake Account detected — {fake_prob}% confidence")
    else:
        st.success(f"✅  Real Account — {real_prob}% confidence")

    pie_df = pd.DataFrame({
        "Category":    ["Real", "Fake"],
        "Probability": [real_prob, fake_prob]
    })

    fig = px.pie(
        pie_df,
        names="Category",
        values="Probability",
        title="Prediction Probability",
        color="Category",
        color_discrete_map={"Real": "#22c55e", "Fake": "#cc0000"},
        hole=0.45
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono", color="#cc0000"),
        title_font=dict(family="Space Grotesk", size=15, color="#cc0000"),
        legend=dict(font=dict(size=12, color="#cc0000"))
    )
    fig.update_traces(
        textfont_size=13,
        textfont_color="#ffffff",
        marker=dict(line=dict(color='#ffffff', width=2))
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Bulk Prediction ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="section-title">Bulk Prediction via CSV</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload a CSV file with the same feature columns", type=["csv"])

if uploaded_file:
    bulk_df = pd.read_csv(uploaded_file)
    predictions = model.predict(bulk_df)
    bulk_df["Prediction"] = pd.Series(predictions).map({0: "✅ Real", 1: "⚠️ Fake"})
    st.dataframe(bulk_df, use_container_width=True)

    csv = bulk_df.to_csv(index=False)
    st.download_button(
        "⬇️  Download Results as CSV",
        csv,
        "prediction_results.csv",
        "text/csv"
    )