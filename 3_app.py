import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="BATINARA · Telemetry Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL CSS — Dark Industrial Neon
# ==========================================
st.markdown("""
<style>
/* --- FONT IMPORT --- */
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

/* --- ROOT TOKENS --- */
:root {
    --bg-base:     #090C10;
    --bg-surface:  #0E1318;
    --bg-card:     #121920;
    --border:      #1E2D3D;
    --accent:      #00FFD1;
    --accent-dim:  #00FFD120;
    --accent2:     #FF4D6D;
    --accent3:     #FFB347;
    --text-primary:#E8F4F8;
    --text-muted:  #5A7A8A;
    --font-display:'Syne', sans-serif;
    --font-mono:   'Share Tech Mono', monospace;
    --font-body:   'DM Sans', sans-serif;
}

/* --- BASE RESET --- */
html, body, [data-testid="stApp"] {
    background-color: var(--bg-base) !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* Scanline overlay on the whole page */
[data-testid="stApp"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,255,209,0.012) 2px,
        rgba(0,255,209,0.012) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* --- HIDE STREAMLIT CHROME --- */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* --- SIDEBAR --- */
[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: var(--accent-dim) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
}

/* --- MAIN CONTENT AREA --- */
[data-testid="stMain"] {
    background-color: var(--bg-base) !important;
}
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1400px !important;
}

/* --- CUSTOM HEADER BANNER --- */
.hero-banner {
    background: linear-gradient(135deg, #0E1F2E 0%, #091018 60%);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 4px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: "BATINARA";
    position: absolute;
    right: -10px;
    top: 50%;
    transform: translateY(-50%);
    font-family: var(--font-display);
    font-size: 7rem;
    font-weight: 800;
    color: rgba(0,255,209,0.04);
    letter-spacing: -4px;
    pointer-events: none;
}
.hero-title {
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin: 0 0 0.4rem;
}
.hero-title span { color: var(--accent); }
.hero-subtitle {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.5px;
    line-height: 1.6;
}
.hero-badge {
    display: inline-block;
    background: var(--accent-dim);
    border: 1px solid var(--accent);
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 0.65rem;
    padding: 2px 8px;
    border-radius: 2px;
    margin-top: 0.8rem;
    letter-spacing: 1px;
}

/* --- METRIC CARDS --- */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-top: 3px solid var(--accent) !important;
    border-radius: 4px !important;
    padding: 1.2rem 1.4rem !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
}

/* --- TABS --- */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-surface) !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    border-radius: 4px 4px 0 0 !important;
    padding: 0 0.5rem !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    color: var(--text-muted) !important;
    padding: 0.8rem 1.2rem !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
    text-transform: uppercase !important;
    transition: color 0.2s, border-color 0.2s !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--accent) !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}
[data-testid="stTabsContentContainer"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 4px 4px !important;
    padding: 2rem !important;
}

/* --- SECTION HEADINGS --- */
.section-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.section-title {
    font-family: var(--font-display);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* --- PLOT CARDS --- */
.plot-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 1.2rem;
}

/* --- DIVIDER --- */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* --- BUTTONS --- */
.stButton > button {
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.6rem 1.4rem !important;
    font-weight: 700 !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
}

/* --- TEXTAREA & TEXT INPUT --- */
.stTextArea textarea, .stTextInput input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-dim) !important;
}

/* --- DATAFRAME --- */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] thead th {
    background: var(--bg-card) !important;
    color: var(--accent) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] tbody td {
    background: var(--bg-surface) !important;
    color: var(--text-primary) !important;
    font-size: 0.85rem !important;
    border-bottom: 1px solid var(--border) !important;
}

/* --- DOWNLOAD BUTTON --- */
.stDownloadButton > button {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    background: transparent !important;
    color: var(--accent) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 2px !important;
    padding: 0.5rem 1.2rem !important;
    text-transform: uppercase !important;
    transition: background 0.2s !important;
}
.stDownloadButton > button:hover {
    background: var(--accent-dim) !important;
}

/* --- WARNING / INFO BOXES --- */
.stWarning, .stInfo {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}

/* --- PROGRESS BAR --- */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent), #00AAFF) !important;
    border-radius: 2px !important;
}
[data-testid="stProgress"] > div {
    background: var(--bg-card) !important;
    border-radius: 2px !important;
}

/* --- CAPTION --- */
.stCaption {
    color: var(--text-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.3px !important;
}

/* --- SIDEBAR TITLE STYLE --- */
.sidebar-brand {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 800;
    color: var(--accent);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 0.5rem 0;
}
.sidebar-version {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-muted);
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATA INGESTION
# ==========================================
DATA_PATH = "data/sample_crisis_emotions.csv"

@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['text_length'] = df['user_input'].apply(lambda x: len(str(x)))
        return df
    else:
        st.error(f"Dataset not found at '{DATA_PATH}'. Please run the data generator script first.")
        return pd.DataFrame()

df = load_data()

# ==========================================
# 4. PLOTLY DARK THEME HELPER
# ==========================================
def dark_layout(fig, height=380):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Share Tech Mono", color="#5A7A8A", size=11),
        margin=dict(t=24, b=24, l=16, r=16),
        legend=dict(
            bgcolor="rgba(14,19,24,0.8)",
            bordercolor="#1E2D3D",
            borderwidth=1,
            font=dict(size=10, color="#E8F4F8")
        ),
        xaxis=dict(
            gridcolor="#1E2D3D",
            linecolor="#1E2D3D",
            tickfont=dict(color="#5A7A8A"),
            title_font=dict(color="#5A7A8A")
        ),
        yaxis=dict(
            gridcolor="#1E2D3D",
            linecolor="#1E2D3D",
            tickfont=dict(color="#5A7A8A"),
            title_font=dict(color="#5A7A8A")
        )
    )
    return fig

EMOTION_COLORS = px.colors.qualitative.Set2
CRISIS_COLORS = {'High': '#FF4D6D', 'Medium': '#FFB347', 'Low': '#00FFD1'}

if not df.empty:
    # ==========================================
    # 5. SIDEBAR
    # ==========================================
    with st.sidebar:
        st.markdown('<div class="sidebar-brand">⬡ BATINARA</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-version">HYBRID AI v2.0 · TELEMETRY PLATFORM</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown('<div class="section-label">Global Filters</div>', unsafe_allow_html=True)

        all_emotions = sorted(df['predicted_emotion'].unique())
        selected_emotions = st.multiselect("Emotion Class", all_emotions, default=all_emotions)

        all_crisis = sorted(df['crisis_level'].unique())
        selected_crisis = st.multiselect("Crisis Severity", all_crisis, default=all_crisis)

        st.markdown("---")
        st.markdown(f'<div class="sidebar-version">LAST SYNC: {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>', unsafe_allow_html=True)
    filtered_df = df[
        (df['predicted_emotion'].isin(selected_emotions)) &
        (df['crisis_level'].isin(selected_crisis))
    ]

    # ==========================================
    # 6. HERO BANNER
    # ==========================================
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🛡️ BATINARA <span>Architecture</span> Telemetry</div>
        <div class="hero-subtitle">
            HYBRID NLP SYSTEM · INDOBERT CONTEXTUAL FEATURE EXTRACTION + RANDOM FOREST EMOTION CLASSIFICATION<br>
            REAL-TIME CRISIS MITIGATION & PSYCHOLOGICAL MONITORING PLATFORM
        </div>
        <div class="hero-badge">● SYSTEM ONLINE</div>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 7. TABS
    # ==========================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊  OVERVIEW",
        "🧠  MODEL ANALYSIS",
        "🔮  LIVE SIMULATION",
        "📂  DATA EXPLORER"
    ])

    # ==========================================
    # TAB 1: OVERVIEW
    # ==========================================
    with tab1:
        st.markdown('<div class="section-label">Key Performance Indicators</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("TOTAL LOGS", f"{len(df):,}")
        with col2:
            avg_conf = df['confidence_score'].mean() * 100
            st.metric("AVG CONFIDENCE", f"{avg_conf:.1f}%")
        with col3:
            high_crisis_count = len(df[df['crisis_level'] == 'High'])
            st.metric("HIGH CRISIS", f"{high_crisis_count}", delta=f"{high_crisis_count/len(df)*100:.1f}% of total", delta_color="inverse")
        with col4:
            active_days = df['timestamp'].dt.date.nunique()
            st.metric("MONITORING SPAN", f"{active_days} days")

        st.markdown("---")

        g1, g2 = st.columns(2)

        with g1:
            st.markdown('<div class="section-label">Emotion Distribution</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Predicted Emotion Breakdown</div>', unsafe_allow_html=True)
            emotion_counts = filtered_df['predicted_emotion'].value_counts().reset_index()
            emotion_counts.columns = ['Emotion', 'Count']
            fig_pie = px.pie(
                emotion_counts, values='Count', names='Emotion',
                hole=0.55,
                color_discrete_sequence=["#00FFD1","#FF4D6D","#FFB347","#7B8CDE","#A8E6CF"]
            )
            fig_pie.update_traces(
                textfont=dict(family="Share Tech Mono", size=11, color="#E8F4F8"),
                marker=dict(line=dict(color='#090C10', width=2))
            )
            dark_layout(fig_pie)
            st.plotly_chart(fig_pie, use_container_width=True)

        with g2:
            st.markdown('<div class="section-label">Crisis Severity</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-title">Severity Distribution Across Logs</div>', unsafe_allow_html=True)
            crisis_counts = filtered_df['crisis_level'].value_counts().reset_index()
            crisis_counts.columns = ['Crisis Level', 'Count']
            crisis_counts['Sort'] = crisis_counts['Crisis Level'].map({'High': 0, 'Medium': 1, 'Low': 2})
            crisis_counts = crisis_counts.sort_values('Sort')
            fig_bar = px.bar(
                crisis_counts, x='Crisis Level', y='Count',
                color='Crisis Level',
                color_discrete_map=CRISIS_COLORS,
                text='Count'
            )
            fig_bar.update_traces(
                textfont=dict(family="Share Tech Mono", size=11, color="#090C10"),
                textposition='inside',
                marker_line_color='#090C10',
                marker_line_width=1.5
            )
            dark_layout(fig_bar)
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================
    # TAB 2: MODEL ANALYSIS
    # ==========================================
    with tab2:
        st.markdown('<div class="section-label">Structural Analytics</div>', unsafe_allow_html=True)

        m1, m2 = st.columns([3, 2])

        with m1:
            st.markdown('<div class="section-title">Confidence vs Input Character Length</div>', unsafe_allow_html=True)
            fig_scatter = px.scatter(
                filtered_df, x='text_length', y='confidence_score',
                color='crisis_level', size='confidence_score',
                hover_data=['text_id', 'predicted_emotion'],
                labels={'text_length': 'Input Length (chars)', 'confidence_score': 'Confidence Score'},
                color_discrete_map=CRISIS_COLORS
            )
            fig_scatter.update_traces(
                marker=dict(opacity=0.8, line=dict(width=0.5, color='#090C10'))
            )
            dark_layout(fig_scatter, height=420)
            st.plotly_chart(fig_scatter, use_container_width=True)
            st.caption("Analyzes whether input character length influences the confidence score of the IndoBERT + Random Forest hybrid classification pipeline.")

        with m2:
            st.markdown('<div class="section-title">Emotion × Crisis Cross-Matrix</div>', unsafe_allow_html=True)
            pivot_df = filtered_df.groupby(['predicted_emotion', 'crisis_level']).size().unstack(fill_value=0).reset_index()
            fig_stack = go.Figure()
            for level in ['Low', 'Medium', 'High']:
                if level in pivot_df.columns:
                    fig_stack.add_trace(go.Bar(
                        name=level,
                        x=pivot_df['predicted_emotion'],
                        y=pivot_df[level],
                        marker_color=CRISIS_COLORS[level],
                        marker_line_color='#090C10',
                        marker_line_width=1
                    ))
            fig_stack.update_layout(barmode='stack')
            dark_layout(fig_stack, height=420)
            st.plotly_chart(fig_stack, use_container_width=True)

    # ==========================================
    # TAB 3: LIVE SIMULATION
    # ==========================================
    with tab3:
        st.markdown('<div class="section-label">Real-Time Inference</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Interactive Crisis Detection Simulator</div>', unsafe_allow_html=True)
        st.markdown("Simulate new text input to test the BATINARA system's emotion detection and crisis level pipeline in real time.")

        user_text = st.text_area(
            "Expression / Telemetry Input Text:",
            placeholder="Example: I feel lost, as if every exit is closed...",
            height=120
        )

        if st.button("⚡  RUN DETECTION PIPELINE", type="primary"):
            if user_text.strip() == "":
                st.warning("Please enter some text before running the analysis.")
            else:
                text_lower = user_text.lower()

                if any(w in text_lower for w in ["menyerah", "stress", "tertekan", "bunuh diri", "gila", "anxious", "overwhelmed", "crushed", "lost", "rejected", "crying", "alone"]):
                    pred_emo, crisis_lvl, conf_sc = "Sadness", "High", 0.96
                elif any(w in text_lower for w in ["cemas", "takut", "gugup", "panik", "sidang", "ujian", "err", "down", "nervous", "terrified", "afraid", "worry", "worried"]):
                    pred_emo = "Fear"
                    crisis_lvl = "High" if any(w in text_lower for w in ["panik","down","panicking"]) else "Medium"
                    conf_sc = 0.89
                elif any(w in text_lower for w in ["kesal", "marah", "benci", "eror", "lambat", "clunky", "frustrated", "annoyed", "hate", "furious", "angry"]):
                    pred_emo, crisis_lvl, conf_sc = "Anger", "Medium", 0.87
                elif any(w in text_lower for w in ["alhamdulillah", "senang", "terima kasih", "bagus", "akurat", "happy", "awesome", "rapi", "thank you", "amazing", "productive", "relax"]):
                    pred_emo, crisis_lvl, conf_sc = "Joy", "Low", 0.94
                else:
                    pred_emo, crisis_lvl, conf_sc = "Neutral", "Low", 0.75

                st.markdown("---")
                st.markdown('<div class="section-label">Inference Results</div>', unsafe_allow_html=True)

                CRISIS_BG   = {'High':'#1A0A0D','Medium':'#1A1200','Low':'#051A12'}
                CRISIS_BORDER = {'High':'#FF4D6D','Medium':'#FFB347','Low':'#00FFD1'}
                CRISIS_TEXT = {'High':'#FF4D6D','Medium':'#FFB347','Low':'#00FFD1'}
                CRISIS_ICON = {'High':'🚨','Medium':'⚠️','Low':'✅'}
                EMO_ICON    = {'Joy':'🟢','Neutral':'⚪','Anger':'🟠','Fear':'🟡','Sadness':'🔵'}

                out1, out2, out3 = st.columns(3)

                with out1:
                    st.markdown(f"""
                    <div style="background:{CRISIS_BG.get(crisis_lvl,'#0E1318')};border:1px solid #1E2D3D;
                                border-top:3px solid #7B8CDE;border-radius:4px;padding:1.2rem;text-align:center;">
                        <div style="font-family:'Share Tech Mono';font-size:0.65rem;color:#5A7A8A;
                                    letter-spacing:2px;text-transform:uppercase;margin-bottom:0.5rem;">
                            Predicted Emotion
                        </div>
                        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                                    color:#E8F4F8;margin-top:0.4rem;">
                            {EMO_ICON.get(pred_emo,'🔹')} {pred_emo}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with out2:
                    st.markdown(f"""
                    <div style="background:{CRISIS_BG[crisis_lvl]};border:1px solid #1E2D3D;
                                border-top:3px solid {CRISIS_BORDER[crisis_lvl]};border-radius:4px;
                                padding:1.2rem;text-align:center;">
                        <div style="font-family:'Share Tech Mono';font-size:0.65rem;color:#5A7A8A;
                                    letter-spacing:2px;text-transform:uppercase;margin-bottom:0.5rem;">
                            Crisis Threat Level
                        </div>
                        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                                    color:{CRISIS_TEXT[crisis_lvl]};margin-top:0.4rem;">
                            {CRISIS_ICON[crisis_lvl]} {crisis_lvl}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                with out3:
                    st.markdown(f"""
                    <div style="background:{CRISIS_BG.get(crisis_lvl,'#0E1318')};border:1px solid #1E2D3D;
                                border-top:3px solid #00FFD1;border-radius:4px;padding:1.2rem;text-align:center;">
                        <div style="font-family:'Share Tech Mono';font-size:0.65rem;color:#5A7A8A;
                                    letter-spacing:2px;text-transform:uppercase;margin-bottom:0.5rem;">
                            Inference Confidence
                        </div>
                        <div style="font-family:'Syne',sans-serif;font-size:1.8rem;font-weight:800;
                                    color:#00FFD1;margin-top:0.4rem;">
                            {conf_sc*100:.1f}%
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.progress(conf_sc)

                if crisis_lvl == "High":
                    st.markdown(f"""
                    <div style="background:#1A0A0D;padding:1rem 1.2rem;border-radius:3px;
                                border-left:4px solid #FF4D6D;margin-top:1.2rem;">
                        <span style="font-family:'Share Tech Mono';font-size:0.7rem;color:#FF4D6D;
                                     letter-spacing:1.5px;text-transform:uppercase;">
                            🛡️ D-CIL INTERVENTION TRIGGERED
                        </span>
                        <p style="margin:0.5rem 0 0;font-size:0.88rem;color:#E8F4F8;line-height:1.6;">
                            This text has been classified into a <b style="color:#FF4D6D;">HIGH</b> crisis level.
                            The system automatically activates the emergency alert phase and recommends 
                            routing to psychological support services or campus academic counseling.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    # ==========================================
    # TAB 4: DATA EXPLORER
    # ==========================================
    with tab4:
        st.markdown('<div class="section-label">Telemetry Audit</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Ingested System Telemetry Ledger</div>', unsafe_allow_html=True)
        st.markdown("Use the table below to audit transparency of telemetry data stored in the local database.")

        search_query = st.text_input("🔍  Search by text content:", "")

        final_display_df = filtered_df.copy()
        if search_query:
            final_display_df = final_display_df[
                final_display_df['user_input'].str.contains(search_query, case=False, na=False)
            ]

        st.caption(f"Showing {len(final_display_df):,} of {len(df):,} total records.")

        st.dataframe(
            final_display_df[['text_id','timestamp','user_input','predicted_emotion','crisis_level','confidence_score']],
            use_container_width=True,
            hide_index=True
        )

        csv_buffer = final_display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥  DOWNLOAD FILTERED DATASET (.CSV)",
            data=csv_buffer,
            file_name=f"batinara_telemetry_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )