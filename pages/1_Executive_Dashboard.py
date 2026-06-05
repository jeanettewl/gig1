import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Executive Business Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GLOBAL CSS — Warm Luxury Editorial (UPDATED)
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Instrument+Sans:wght@300;400;500;600&family=Courier+Prime:wght@400;700&display=swap');

:root {
    --cream:       #F5F0E8;
    --cream-dark:  #EDE6D6;
    --parchment:   #E8DFC8;
    --ink:         #1A1208;
    --ink-mid:     #3D3320;
    --ink-muted:   #8C7B5C;
    --gold:        #C4933A;
    --gold-light:  #D4A84B;
    --gold-dim:    rgba(196,147,58,0.12);
    --rust:        #B54A2A;
    --sage:        #4A6741;
    --border:      rgba(196,147,58,0.25);
    --border-soft: rgba(26,18,8,0.1);
    --font-serif:  'Playfair Display', Georgia, serif;
    --font-sans:   'Instrument Sans', sans-serif;
    --font-mono:   'Courier Prime', monospace;
}

/* BASE */
html, body, [data-testid="stApp"] {
    background-color: var(--cream) !important;
    font-family: var(--font-sans) !important;
    color: var(--ink) !important;
}

/* Subtle grain texture overlay */
[data-testid="stApp"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9998;
    opacity: 0.5;
}

/* HIDE STREAMLIT CHROME */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* MAIN AREA */
[data-testid="stMain"] { background-color: var(--cream) !important; }
.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1440px !important;
}

/* SIDEBAR REFACTOR (Fixed low contrast text issue) */
[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: 1px solid rgba(196,147,58,0.2) !important;
}

/* Menargetkan teks deskriptif umum di dalam sidebar tanpa menimpa judul */
[data-testid="stSidebar"] p { 
    color: var(--cream-dark) !important; 
}

/* Memperbaiki style komponen multiselect */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: var(--gold-dim) !important;
    border: 1px solid var(--gold) !important;
    color: var(--gold-light) !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div {
    background: #2A2010 !important;
    border-color: rgba(196,147,58,0.3) !important;
}

/* Memperbaiki kontras input tanggal (Temporal Scope) */
[data-testid="stSidebar"] .stDateInput input {
    background: #2A2010 !important;
    color: var(--cream) !important;
    border-color: rgba(196,147,58,0.3) !important;
}

[data-testid="stSidebar"] hr { border-color: rgba(196,147,58,0.2) !important; }

/* Menyeragamkan seluruh label input di sidebar */
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] label p { 
    color: #B89A6A !important; 
    font-size: 0.75rem !important; 
    letter-spacing: 1px !important; 
    text-transform: uppercase !important; 
    font-family: 'Courier Prime', monospace !important; 
    font-weight: bold !important;
}

/* SIDEBAR DOWNLOAD BUTTON (Fixed text visibility) */
[data-testid="stSidebar"] .stDownloadButton > button {
    background: transparent !important;
    color: var(--gold-light) !important;
    border: 1px solid rgba(196,147,58,0.4) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.5px !important;
    width: 100% !important;
    border-radius: 2px !important;
    padding: 0.5rem !important;
    transition: background 0.2s !important;
}
[data-testid="stSidebar"] .stDownloadButton > button:hover {
    background: rgba(196,147,58,0.1) !important;
}
[data-testid="stSidebar"] .stDownloadButton button p {
    color: var(--gold-light) !important;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background: var(--cream-dark) !important;
    border: 1px solid var(--border) !important;
    border-top: 3px solid var(--gold) !important;
    border-radius: 2px !important;
    padding: 1.4rem 1.5rem !important;
    position: relative !important;
}
[data-testid="stMetricLabel"] {
    font-family: var(--font-mono) !important;
    font-size: 0.62rem !important;
    color: var(--ink-muted) !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="stMetricValue"] {
    font-family: var(--font-serif) !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
    letter-spacing: -0.5px !important;
}
[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    color: var(--sage) !important;
}

/* Fix any stray white text in main content area */
[data-testid="stMain"] p,
[data-testid="stMain"] span,
[data-testid="stMain"] div,
[data-testid="stMain"] li {
    color: var(--ink-mid);
}
[data-testid="stMain"] strong,
[data-testid="stMain"] b {
    color: var(--ink) !important;
}

/* CONTAINERS WITH BORDER */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--cream-dark) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 2px !important;
    padding: 1.2rem !important;
}

/* HEADINGS */
h1, h2, h3, h4, h5 {
    font-family: var(--font-serif) !important;
    color: var(--ink) !important;
}

/* SUBHEADER */
[data-testid="stSubheader"] h3 {
    font-family: var(--font-serif) !important;
    font-size: 1.3rem !important;
    color: var(--ink) !important;
    border-bottom: 1px solid var(--border) !important;
    padding-bottom: 0.5rem !important;
}

/* DIVIDER */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* INFO / SUCCESS / WARNING / ERROR BOXES */
[data-testid="stAlert"] {
    border-radius: 2px !important;
    border-left-width: 3px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] li,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div,
[data-testid="stAlert"] * {
    color: var(--ink-mid) !important;
    font-family: var(--font-sans) !important;
}
[data-testid="stAlert"] strong {
    color: var(--ink) !important;
    font-weight: 600 !important;
}
.stInfo {
    background: rgba(196,147,58,0.1) !important;
    border-left-color: var(--gold) !important;
}
.stSuccess {
    background: rgba(74,103,65,0.1) !important;
    border-left-color: var(--sage) !important;
}
.stWarning {
    background: rgba(181,74,42,0.09) !important;
    border-left-color: var(--rust) !important;
}
.stError {
    background: rgba(181,74,42,0.12) !important;
    border-left-color: var(--rust) !important;
}

/* DOWNLOAD BUTTON (main area) */
.stDownloadButton > button {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    background: var(--ink) !important;
    color: var(--gold-light) !important;
    border: 1px solid var(--gold) !important;
    border-radius: 2px !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
.stDownloadButton > button:hover { opacity: 0.85 !important; }

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
}
[data-testid="stDataFrame"] thead th {
    background: var(--parchment) !important;
    color: var(--ink-muted) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}
[data-testid="stDataFrame"] tbody td {
    font-family: var(--font-sans) !important;
    font-size: 0.85rem !important;
    color: var(--ink-mid) !important;
}

/* SECTION LABELS */
.sec-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    letter-spacing: 3px;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.sec-title {
    font-family: var(--font-serif);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border);
}

/* SIDEBAR BRAND BRANDING STRUCTURE */
.sb-brand {
    font-family: var(--font-serif);
    font-size: 1.5rem;
    font-weight: bold;
    color: #C4933A !important; /* Diubah ke krem kontras agar menyala di background gelap */
}
.sb-sub {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: #C4933A !important; /* Diubah ke warna emas agar senada dengan tema */
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. DATA LOAD
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("business_sales_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("File 'business_sales_data.csv' not found. Please run the data generator script first.")
    st.stop()

# ==========================================
# 4. PLOTLY WARM THEME HELPER
# ==========================================
def warm_layout(fig, height=320):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Courier Prime, monospace", color="#8C7B5C", size=11),
        margin=dict(t=20, b=20, l=12, r=12),
        legend=dict(
            bgcolor="rgba(232,223,200,0.8)",
            bordercolor="rgba(196,147,58,0.3)",
            borderwidth=1,
            font=dict(color="#3D3320", size=10)
        ),
        xaxis=dict(
            gridcolor="rgba(196,147,58,0.12)",
            linecolor="rgba(196,147,58,0.2)",
            tickfont=dict(color="#8C7B5C", family="Courier Prime")
        ),
        yaxis=dict(
            gridcolor="rgba(196,147,58,0.12)",
            linecolor="rgba(196,147,58,0.2)",
            tickfont=dict(color="#8C7B5C", family="Courier Prime")
        )
    )
    return fig

# ==========================================
# 5. SIDEBAR
# ==========================================
with st.sidebar:
    # Menggunakan class .sb-brand dan .sb-sub yang sudah di-fix di blok CSS atas
    st.markdown('<div class="sb-brand">Executive Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-sub">Operational Parameters</div>', unsafe_allow_html=True)
    st.markdown("---")

    # Komponen Multiselect
    all_regions = df['Region'].unique().tolist()
    selected_regions = st.multiselect("Target Region(s)", options=all_regions, default=all_regions)
    
    min_date = df['Date'].min().to_pydatetime()
    max_date = df['Date'].max().to_pydatetime()
    
    selected_date_range = st.date_input(
        "Temporal Scope",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filter Logic
    filtered_df = df[df['Region'].isin(selected_regions)]
    if isinstance(selected_date_range, tuple) and len(selected_date_range) == 2:
        s, e = selected_date_range
        filtered_df = filtered_df[
            (filtered_df['Date'] >= pd.to_datetime(s)) &
            (filtered_df['Date'] <= pd.to_datetime(e))
        ]

    if not filtered_df.empty:
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.markdown("---")
        st.download_button(
            label="↓ Download Filtered Data (.CSV)",
            data=csv_data,
            file_name='filtered_business_data.csv',
            mime='text/csv',
            key='sidebar_download'
        )

# ==========================================
# 6. HERO HEADER
# ==========================================
st.markdown("""
<div style="border-left: 4px solid #C4933A; padding: 1.2rem 2rem; margin-bottom: 2rem;
            background: linear-gradient(135deg, #EDE6D6 0%, #F5F0E8 100%);
            border-radius: 2px; position: relative; overflow: hidden;">
    <div style="position:absolute;right:2rem;top:50%;transform:translateY(-50%);
                font-family:'Playfair Display',serif;font-size:5rem;font-weight:900;
                color:rgba(196,147,58,0.20);letter-spacing:-4px;pointer-events:none;">
        ENTERPRISE
    </div>
    <div style="font-family:'Courier Prime',monospace;font-size:0.62rem;color:#C4933A;
                letter-spacing:3px;text-transform:uppercase;margin-bottom:0.4rem;">
        Performance Architecture
    </div>
    <div style="font-family:'Playfair Display',serif;font-size:1.9rem;font-weight:700;
                color:#1A1208;line-height:1.2;margin-bottom:0.3rem;">
        Executive Business Dashboard
    </div>
    <div style="font-family:'Instrument Sans',sans-serif;font-size:0.85rem;color:#8C7B5C;">
        Automated operational run-rate optimization &amp; performance mapping framework
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. KPI METRICS
# ==========================================
st.markdown('<div class="sec-label">Key Performance Indicators</div>', unsafe_allow_html=True)

total_revenue = filtered_df['Revenue'].sum() if not filtered_df.empty else 0
total_users   = filtered_df['Active_Users'].sum() if not filtered_df.empty else 0
avg_users     = filtered_df['Active_Users'].mean() if not filtered_df.empty else 0
total_conv    = filtered_df['Conversions'].sum() if not filtered_df.empty else 0
global_conv_rate = (total_conv / total_users * 100) if total_users > 0 else 0

k1, k2, k3, k4 = st.columns(4)
with k1:
    with st.container(border=True):
        st.metric("Aggregate Revenue", f"${total_revenue:,.2f}",
                  delta="Target Envelope Met" if total_revenue > 0 else None)
with k2:
    with st.container(border=True):
        st.metric("Cumulative Active Users", f"{total_users:,}",
                  delta="Nominal Traffic Core" if total_users > 0 else None)
with k3:
    with st.container(border=True):
        st.metric("Mean Daily Traffic", f"{int(avg_users):,}",
                  delta="Steady Operational State" if avg_users > 0 else None)
with k4:
    with st.container(border=True):
        st.metric("Avg Conversion Rate", f"{global_conv_rate:.2f}%",
                  delta="Optimization Benchmark" if global_conv_rate > 0 else None)

# ==========================================
# 8. LIVE INSIGHTS
# ==========================================
st.markdown("---")

if not filtered_df.empty:
    best_source = filtered_df.groupby('Lead_Source')['Revenue'].sum().idxmax()
    best_region = filtered_df.groupby('Region')['Revenue'].sum().idxmax()

    ins_col, alert_col = st.columns([2, 1])

    with ins_col:
        st.info(f"""
💡 **Automated Tactical Summary**
- High-Yield Acquisition Channel: **{best_source}** — primary structural revenue driver.
- Dominant Operational Territory: Performance peak at **{best_region}** sector.
        """)

    with alert_col:
        daily_rev = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
        if not daily_rev.empty:
            avg_daily = daily_rev['Revenue'].mean()
            latest_rev = daily_rev['Revenue'].iloc[-1]
            latest_date = daily_rev['Date'].iloc[-1].strftime('%b %d, %Y')
            if latest_rev < (avg_daily * 0.75):
                st.error(f"🚨 **Anomalous Variance ({latest_date}):** Revenue baseline breached — ${latest_rev:,.2f}.")
            else:
                st.success(f"✅ **System Nominal ({latest_date}):** Operational tracing stable against mean indicators.")
else:
    st.warning("No data clusters captured. Adjust operational filters.")

# ==========================================
# 9. PREDICTIVE ANALYTICS
# ==========================================
st.markdown("---")
st.markdown('<div class="sec-label">Advanced Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Predictive Modeling & Matrix Analytics</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    pred_c1, pred_c2 = st.columns(2)

    with pred_c1:
        with st.container(border=True):
            st.markdown('<div class="sec-label">30-Day Forecast</div>', unsafe_allow_html=True)
            st.markdown("**Algorithmic Sales Run-Rate**")
            forecast_df = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
            forecast_df['7_Day_MA'] = forecast_df['Revenue'].rolling(window=7, min_periods=1).mean()
            last_ma = forecast_df['7_Day_MA'].iloc[-1] if not forecast_df.empty else 0
            projected = last_ma * 30 * 1.03
            st.caption("Projected runway using 7-day rolling average with efficiency scale factor:")
            st.metric("Calculated Forward Runway", f"${projected:,.2f}", delta="+3.0% Efficiency Scale")

    with pred_c2:
        with st.container(border=True):
            st.markdown('<div class="sec-label">RPU Yield Matrix</div>', unsafe_allow_html=True)
            st.markdown("**Revenue Per User by Channel**")
            rpu_df = filtered_df.groupby('Lead_Source').agg({'Revenue':'sum','Active_Users':'sum'}).reset_index()
            rpu_df['RPU'] = rpu_df['Revenue'] / rpu_df['Active_Users'].replace(0, 1)
            rpu_df = rpu_df.sort_values('RPU', ascending=False)
            best_chan = rpu_df['Lead_Source'].iloc[0]
            best_val  = rpu_df['RPU'].iloc[0]
            st.caption("Tracking which acquisition pipeline generates the highest monetary conversion per user:")
            st.success(f"💎 **Top Node:** **{best_chan}** yields **${best_val:.2f} / user**")

    # Velocity
    with st.container(border=True):
        st.markdown('<div class="sec-label">Velocity Analytics</div>', unsafe_allow_html=True)
        st.markdown("**Short-Term Rolling Momentum vs Historical Baseline**")
        daily_perf = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
        if len(daily_perf) >= 7:
            recent_avg  = daily_perf['Revenue'].tail(7).mean()
            hist_avg    = daily_perf['Revenue'].mean()
            velocity    = ((recent_avg - hist_avg) / hist_avg) * 100
            st.caption("Evaluating whether 7-day performance acceleration exceeds the long-term baseline:")
            if velocity > 0:
                st.info(f"📈 **Positive Momentum:** Last 7 days running **{velocity:.2f}% faster** than historical average.")
            else:
                st.warning(f"📉 **Deceleration Warning:** Sales slowed **{abs(velocity):.2f}% below** historical baseline.")
        else:
            st.caption("Insufficient data to calculate rolling momentum (minimum 7-day range required).")

else:
    st.warning("Predictive framework inactive. Ensure filters isolate historical data points.")

# ==========================================
# 10. CHARTS
# ==========================================
st.markdown("---")
st.markdown('<div class="sec-label">Data Visualizations</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Performance Intelligence Charts</div>', unsafe_allow_html=True)

ch1, ch2 = st.columns(2)

with ch1:
    with st.container(border=True):
        st.markdown('<div class="sec-label">Revenue Trend</div>', unsafe_allow_html=True)
        st.markdown("**Operational Revenue (Spline Curve)**")
        if not filtered_df.empty:
            trend_df = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=trend_df['Date'], y=trend_df['Revenue'],
                mode='lines',
                line=dict(shape='spline', color='#C4933A', width=2.5),
                fill='tozeroy',
                fillcolor='rgba(196,147,58,0.08)',
                name='Revenue',
                hovertemplate="<b>%{x|%b %d}</b><br>$%{y:,.2f}<extra></extra>"
            ))
            warm_layout(fig_line, height=310)
            st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("No trend data available.")

with ch2:
    with st.container(border=True):
        st.markdown('<div class="sec-label">Channel Distribution</div>', unsafe_allow_html=True)
        st.markdown("**Volume by Acquisition Channel**")
        if not filtered_df.empty:
            src_df = filtered_df.groupby('Lead_Source')['Revenue'].sum().reset_index().sort_values('Revenue', ascending=True)
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                x=src_df['Revenue'], y=src_df['Lead_Source'],
                orientation='h',
                marker=dict(
                    color=src_df['Revenue'],
                    colorscale=[[0, '#E8DFC8'], [0.5, '#C4933A'], [1, '#8A5C1A']],
                    line=dict(color='rgba(196,147,58,0.3)', width=0.8)
                ),
                hovertemplate="<b>%{y}</b><br>$%{x:,.2f}<extra></extra>"
            ))
            warm_layout(fig_bar, height=310)
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("No distribution data available.")

# ==========================================
# 11. DATA EXPLORER
# ==========================================
st.markdown("---")
st.markdown('<div class="sec-label">Granular Audit</div>', unsafe_allow_html=True)
st.markdown('<div class="sec-title">Data Explorer Matrix</div>', unsafe_allow_html=True)

if not filtered_df.empty:
    with st.container(border=True):
        st.caption(f"Showing {len(filtered_df):,} records · sorted by date descending")
        st.dataframe(
            filtered_df.sort_values('Date', ascending=False),
            use_container_width=True,
            hide_index=True,
            height=260
        )
        final_csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="↓ Export Enterprise Data Matrix (.CSV)",
            data=final_csv,
            file_name='filtered_business_data.csv',
            mime='text/csv',
            key='main_download'
        )
else:
    st.warning("Operational data empty. Adjust filters to retrieve records.")