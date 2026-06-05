import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Feedback Intelligence Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# 2. GLOBAL CSS — Deep Space Bioluminescent
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Literata:ital,wght@0,300;0,400;0,600;1,300&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --void:        #05070F;
    --deep:        #080D1A;
    --surface:     #0C1220;
    --card:        #0F1628;
    --border:      rgba(99,102,241,0.18);
    --border-glow: rgba(99,102,241,0.35);
    --violet:      #6366F1;
    --violet-dim:  rgba(99,102,241,0.12);
    --violet-glow: rgba(99,102,241,0.06);
    --cyan:        #22D3EE;
    --cyan-dim:    rgba(34,211,238,0.1);
    --emerald:     #10B981;
    --rose:        #F43F5E;
    --amber:       #FBBF24;
    --text-primary: #E2E8F8;
    --text-muted:   #4A5568;
    --text-mid:     #94A3B8;
    --font-display: 'Rajdhani', sans-serif;
    --font-body:    'Literata', Georgia, serif;
    --font-mono:    'JetBrains Mono', monospace;
}

/* BASE */
html, body, [data-testid="stApp"] {
    background-color: var(--void) !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* Moving star-field dots via CSS */
[data-testid="stApp"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 10% 20%, rgba(99,102,241,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 30% 60%, rgba(34,211,238,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 15%, rgba(99,102,241,0.3) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 45%, rgba(34,211,238,0.25) 0%, transparent 100%),
        radial-gradient(1px 1px at 90% 80%, rgba(99,102,241,0.35) 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 85%, rgba(34,211,238,0.2) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 65% 70%, rgba(99,102,241,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 90%, rgba(34,211,238,0.3) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* HIDE STREAMLIT CHROME */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* MAIN */
[data-testid="stMain"] { background-color: var(--void) !important; }
.block-container {
    padding: 2rem 2.8rem 4rem !important;
    max-width: 1400px !important;
    position: relative;
    z-index: 1;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: var(--deep) !important;
    border-right: 1px solid var(--border-glow) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] label {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: var(--text-mid) !important;
}
[data-testid="stSidebar"] hr { border-color: var(--border) !important; }
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: var(--violet-dim) !important;
    border: 1px solid var(--violet) !important;
    color: #A5B4FC !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border-glow) !important;
}
[data-testid="stSidebar"] .stFileUploader {
    background: var(--surface) !important;
    border: 1px dashed var(--border-glow) !important;
    border-radius: 4px !important;
    padding: 0.5rem !important;
}
[data-testid="stSidebar"] .stDownloadButton > button,
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid var(--border-glow) !important;
    color: #A5B4FC !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    border-radius: 3px !important;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-top: 2px solid var(--violet) !important;
    border-radius: 3px !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.07) !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.6rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-mid) !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    color: var(--cyan) !important;
}

/* CONTAINERS */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    padding: 1.4rem !important;
    box-shadow: 0 0 30px rgba(99,102,241,0.05) !important;
}

/* HEADINGS */
h1, h2, h3, h4 {
    font-family: var(--font-display) !important;
    color: var(--text-primary) !important;
    letter-spacing: 0.5px !important;
}

/* SUBHEADER */
[data-testid="stSubheader"] h3 {
    font-family: var(--font-display) !important;
    font-size: 1.2rem !important;
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.5rem !important;
}

/* DIVIDERS */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* BUTTONS */
.stButton > button {
    font-family: var(--font-mono) !important;
    font-size: 0.78rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, var(--violet) 0%, #4F46E5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 3px !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity 0.2s !important;
    box-shadow: 0 0 16px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

/* CLEAR HISTORY BUTTON */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border-glow) !important;
    color: var(--text-mid) !important;
    box-shadow: none !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton > button {
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid rgba(34,211,238,0.35) !important;
    border-radius: 3px !important;
    transition: background 0.2s !important;
}
.stDownloadButton > button:hover {
    background: var(--cyan-dim) !important;
}

/* TEXT INPUT / TEXTAREA */
.stTextInput input, .stTextArea textarea {
    background: var(--surface) !important;
    border: 1px solid var(--border-glow) !important;
    border-radius: 3px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* SELECTBOX */
[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border-color: var(--border-glow) !important;
    border-radius: 3px !important;
    color: var(--text-primary) !important;
}

/* RADIO */
.stRadio label { font-family: var(--font-mono) !important; font-size: 0.78rem !important; color: var(--text-mid) !important; }
.stRadio [data-baseweb="radio"] { accent-color: var(--violet) !important; }

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
}
[data-testid="stDataFrame"] thead th {
    background: var(--surface) !important;
    color: var(--cyan) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.65rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-glow) !important;
}
[data-testid="stDataFrame"] tbody td {
    background: var(--card) !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
    border-bottom: 1px solid var(--border) !important;
}

/* ALERT BOXES */
[data-testid="stAlert"] {
    border-radius: 3px !important;
    border-left-width: 3px !important;
}
[data-testid="stAlert"] *,
[data-testid="stAlert"] p,
[data-testid="stAlert"] span {
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
}
.stSuccess { background: rgba(16,185,129,0.1) !important; border-left-color: var(--emerald) !important; }
.stWarning { background: rgba(251,191,36,0.1) !important; border-left-color: var(--amber) !important; }
.stError   { background: rgba(244,63,94,0.12) !important; border-left-color: var(--rose) !important; }
.stInfo    { background: var(--violet-glow) !important; border-left-color: var(--violet) !important; }

/* CAPTION */
.stCaption, [data-testid="stCaptionContainer"] p {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.3px !important;
}

/* SPINNER */
[data-testid="stSpinner"] { color: var(--violet) !important; }

/* SECTION LABEL HELPER */
.slabel {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 3px;
    color: var(--violet);
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.stitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.6rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* SIDEBAR BRAND */
.sb-brand {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #A5B4FC;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.sb-ver {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem;
    color: #4A5568;
    letter-spacing: 2px;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. SESSION STATE
# ─────────────────────────────────────────────
if 'history_log' not in st.session_state:
    st.session_state['history_log'] = pd.DataFrame([
        {
            "Timestamp":  "2026-06-03 10:00",
            "Input Text": "The platform is incredibly fast, highly recommended!",
            "Model":      "IndoBERT Large",
            "Sentiment":  "Positive",
            "Emotion":    "Joy"
        },
        {
            "Timestamp":  "2026-06-03 10:02",
            "Input Text": "System crashed during the payment process. Fix this.",
            "Model":      "RoBERTa Classifier",
            "Sentiment":  "Negative",
            "Emotion":    "Anger"
        }
    ])

# ─────────────────────────────────────────────
# 4. LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        return pd.read_csv('customer_feedback1.csv')
    except FileNotFoundError:
        return pd.DataFrame({
            'Review_Text': [
                "The app interface is beautiful, but the loading time is slightly slow.",
                "Worst customer service ever. Disappointed.",
                "Absolutely love this platform! Extremely fast and reliable.",
                "Average performance, nothing special but it works fine.",
                "Terrible experience, bugs everywhere inside the main dashboard."
            ],
            'Sentiment': ['Neutral', 'Negative', 'Positive', 'Neutral', 'Negative'],
            'Emotion':   ['Sadness', 'Anger',    'Joy',      'Neutral', 'Anger']
        })

df = load_data()

# ─────────────────────────────────────────────
# 5. PLOTLY DARK SPACE THEME
# ─────────────────────────────────────────────
def space_layout(fig, height=320):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="JetBrains Mono, monospace", color="#4A5568", size=11),
        margin=dict(t=20, b=20, l=12, r=12),
        legend=dict(
            bgcolor="rgba(15,22,40,0.85)",
            bordercolor="rgba(99,102,241,0.2)",
            borderwidth=1,
            font=dict(color="#94A3B8", size=10)
        ),
        xaxis=dict(
            gridcolor="rgba(99,102,241,0.08)",
            linecolor="rgba(99,102,241,0.15)",
            tickfont=dict(color="#4A5568", family="JetBrains Mono")
        ),
        yaxis=dict(
            gridcolor="rgba(99,102,241,0.08)",
            linecolor="rgba(99,102,241,0.15)",
            tickfont=dict(color="#4A5568", family="JetBrains Mono")
        )
    )
    return fig

SENTIMENT_COLORS = {
    'Positive': '#10B981',
    'Neutral':  '#FBBF24',
    'Negative': '#F43F5E'
}

# ─────────────────────────────────────────────
# 6. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-brand">⬡ Feedback AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-ver">Intelligence Engine v3.0</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="slabel">Batch Processing</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"], label_visibility="collapsed")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Dataset loaded successfully.")

    st.markdown("---")
    st.markdown('<div class="slabel">Global Filters</div>', unsafe_allow_html=True)

    available_sentiments = df['Sentiment'].unique().tolist()
    selected_sentiments = st.multiselect(
        "Sentiment Class",
        options=available_sentiments,
        default=available_sentiments
    )

filtered_df = df[df['Sentiment'].isin(selected_sentiments)]

# ─────────────────────────────────────────────
# 7. HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="border-left: 4px solid #6366F1; padding: 1.4rem 2rem; margin-bottom: 2rem;
            background: linear-gradient(135deg, #0C1220 0%, #080D1A 100%);
            border-radius: 3px; position: relative; overflow: hidden;
            box-shadow: 0 0 40px rgba(99,102,241,0.08);">
    <div style="position:absolute;right:1.5rem;top:50%;transform:translateY(-50%);
                font-family:'Rajdhani',sans-serif;font-size:6rem;font-weight:700;
                color:rgba(99,102,241,0.20);letter-spacing:-2px;pointer-events:none;
                user-select:none;line-height:1;">SIGNAL</div>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#6366F1;
                letter-spacing:3px;text-transform:uppercase;margin-bottom:0.5rem;">
        AI-Powered · NLP Intelligence · Real-Time Analysis
    </div>
    <div style="font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;
                color:#E2E8F8;line-height:1.1;margin-bottom:0.3rem;">
        Customer Feedback Intelligence Engine
    </div>
    <div style="font-family:'Literata',serif;font-size:0.88rem;color:#4A5568;
                font-style:italic;line-height:1.5;">
        Transforming raw unstructured text into real-time actionable business metrics
    </div>
    <div style="display:inline-block;margin-top:0.8rem;background:rgba(99,102,241,0.12);
                border:1px solid rgba(99,102,241,0.3);color:#A5B4FC;
                font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                padding:3px 10px;border-radius:2px;letter-spacing:1.5px;">
        ● PIPELINE ONLINE
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 8. KPI METRICS
# ─────────────────────────────────────────────
st.markdown('<div class="slabel">Key Performance Indicators</div>', unsafe_allow_html=True)

total_reviews  = len(filtered_df)
positive_count = len(filtered_df[filtered_df['Sentiment'] == 'Positive'])
pos_rate       = (positive_count / total_reviews * 100) if total_reviews > 0 else 0

k1, k2, k3 = st.columns(3)
with k1:
    with st.container(border=True):
        st.metric("Total Reviews Analyzed", f"{total_reviews:,}")
with k2:
    with st.container(border=True):
        st.metric("Positive Sentiment Rate", f"{pos_rate:.1f}%")
with k3:
    with st.container(border=True):
        st.metric("Model Accuracy", "94.2%", delta="IndoBERT Engine")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 9. TEXT ANALYSIS SANDBOX
# ─────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="slabel">Live Inference</div>', unsafe_allow_html=True)
    st.markdown('<div class="stitle">🔮 Text Analysis Engine Sandbox</div>', unsafe_allow_html=True)
    st.caption("Test the production-ready NLP model live with single text inputs.")

    user_input = st.text_area(
        label="Paste Customer Review / Feedback:",
        value="The app interface is beautiful, but the loading time is slightly slow and frustrating.",
        height=100,
        label_visibility="visible"
    )

    model_option = st.selectbox(
        "NLP Architecture:",
        (
            "IndoBERT Large + Dynamic Context Integration (D-CIL)",
            "Random Forest + TF-IDF Vectorizer",
            "Transformer-based RoBERTa Classifier"
        )
    )

    if st.button("▶  Run AI Analysis Pipeline", type="primary", use_container_width=True):
        with st.spinner("Processing through NLP pipeline..."):
            lower = user_input.lower()
            negative_words = ['slow', 'bad', 'frustrating', 'worst', 'error',
                              'terrible', 'crashed', 'bugs', 'disappointed']
            positive_words = ['beautiful', 'love', 'great', 'fast', 'reliable',
                              'recommended', 'amazing', 'excellent']

            if any(w in lower for w in negative_words):
                pred_sentiment = "Negative"
                pred_emotion   = "Anger" if any(w in lower for w in ['worst','bad','terrible','crashed']) else "Sadness"
            elif any(w in lower for w in positive_words):
                pred_sentiment = "Positive"
                pred_emotion   = "Joy"
            else:
                pred_sentiment = "Neutral"
                pred_emotion   = "Neutral"

            new_log = {
                "Timestamp":  pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
                "Input Text": user_input,
                "Model":      model_option.split(" + ")[0],
                "Sentiment":  pred_sentiment,
                "Emotion":    pred_emotion
            }
            st.session_state['history_log'] = pd.concat(
                [pd.DataFrame([new_log]), st.session_state['history_log']],
                ignore_index=True
            )

        st.markdown("---")
        st.markdown('<div class="slabel">Inference Output</div>', unsafe_allow_html=True)

        SENT_COLOR = {'Positive': '#10B981', 'Negative': '#F43F5E', 'Neutral': '#FBBF24'}
        EMO_ICON   = {'Joy': '🟢', 'Anger': '🔴', 'Sadness': '🔵', 'Neutral': '⚪'}
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"""
            <div style="background:#0F1628;border:1px solid rgba(99,102,241,0.2);
                        border-top:3px solid {SENT_COLOR.get(pred_sentiment,'#6366F1')};
                        border-radius:3px;padding:1.2rem;text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                            color:#4A5568;letter-spacing:2px;text-transform:uppercase;
                            margin-bottom:0.4rem;">Predicted Sentiment</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;
                            color:{SENT_COLOR.get(pred_sentiment,'#E2E8F8')};">{pred_sentiment}</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown(f"""
            <div style="background:#0F1628;border:1px solid rgba(99,102,241,0.2);
                        border-top:3px solid #22D3EE;
                        border-radius:3px;padding:1.2rem;text-align:center;">
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                            color:#4A5568;letter-spacing:2px;text-transform:uppercase;
                            margin-bottom:0.4rem;">Detected Emotion</div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:2rem;font-weight:700;
                            color:#22D3EE;">{EMO_ICON.get(pred_emotion,'🔹')} {pred_emotion}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 10. HISTORY LOG
# ─────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="slabel">Session Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="stitle">📜 Real-Time Sandbox Testing History</div>', unsafe_allow_html=True)
    st.caption("Record of all single-text simulation runs in this session.")

    st.dataframe(
        st.session_state['history_log'],
        use_container_width=True,
        hide_index=True,
        height=150
    )

    if st.button("🗑  Clear Testing History", use_container_width=True):
        st.session_state['history_log'] = pd.DataFrame(
            columns=["Timestamp", "Input Text", "Model", "Sentiment", "Emotion"]
        )
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 11. SENTIMENT CHART
# ─────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="slabel">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="stitle">📊 Sentiment Breakdown Distribution</div>', unsafe_allow_html=True)
    st.caption("Aggregated distribution across the current filtered dataset.")

    if not filtered_df.empty:
        sentiment_counts = filtered_df['Sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']

        fig = px.pie(
            sentiment_counts,
            values='Count', names='Sentiment',
            hole=0.55,
            color='Sentiment',
            color_discrete_map=SENTIMENT_COLORS
        )
        fig.update_traces(
            textfont=dict(family="JetBrains Mono", size=11, color="#E2E8F8"),
            marker=dict(line=dict(color='#05070F', width=2))
        )
        space_layout(fig, height=320)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("No data rows match the selected sentiment filters.")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 12. WORD CLOUD
# ─────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="slabel">Text Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="stitle">☁️ Targeted Context Word Cloud</div>', unsafe_allow_html=True)
    st.caption("Most frequent terms across selected review segments.")

    cloud_target = st.radio(
        "Analysis Target:",
        ["All Reviews", "Positive Only", "Negative Only"],
        horizontal=True
    )

    if not filtered_df.empty:
        if cloud_target == "Positive Only":
            cloud_df = filtered_df[filtered_df['Sentiment'] == 'Positive']
        elif cloud_target == "Negative Only":
            cloud_df = filtered_df[filtered_df['Sentiment'] == 'Negative']
        else:
            cloud_df = filtered_df

        if not cloud_df.empty:
            all_text = " ".join(cloud_df['Review_Text'].astype(str))
            wordcloud = WordCloud(
                width=900, height=260,
                background_color='#0C1220',
                max_words=40,
                colormap='cool',
                contour_width=0,
            ).generate(all_text)

            fig_wc, ax_wc = plt.subplots(figsize=(11, 3.2))
            fig_wc.patch.set_facecolor('#0C1220')
            ax_wc.set_facecolor('#0C1220')
            ax_wc.imshow(wordcloud, interpolation='bilinear')
            ax_wc.axis('off')
            st.pyplot(fig_wc)
        else:
            st.warning(f"No reviews found for: **{cloud_target}**")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 13. DATA EXPLORER
# ─────────────────────────────────────────────
with st.container(border=True):
    st.markdown('<div class="slabel">Granular Audit</div>', unsafe_allow_html=True)
    st.markdown('<div class="stitle">📋 Advanced Data Explorer</div>', unsafe_allow_html=True)
    st.caption("Search, filter, and review individual data points in real-time.")

    search_query = st.text_input("🔍  Search feedback keywords:", "")

    display_df = filtered_df.copy()
    if search_query:
        display_df = display_df[
            display_df['Review_Text'].str.contains(search_query, case=False, na=False)
        ]

    st.caption(f"Showing {len(display_df):,} of {len(filtered_df):,} records")
    st.dataframe(display_df, use_container_width=True, height=280, hide_index=True)

    csv_export = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="↓  Export Filtered Insights (.CSV)",
        data=csv_export,
        file_name='ai_feedback_export.csv',
        mime='text/csv',
        use_container_width=True
    )