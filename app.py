import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Data Science & Engineering Portfolio",
    page_icon="💼",
    layout="wide"
)

# Custom Styling for the Hub
st.markdown("""
    <style>
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #F8FAFC; }
    .project-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #334155;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.title("💼 Enterprise Data Architecture & NLP Portfolio")
st.markdown("### Welcome to my production-grade engineering repository.")
st.markdown("Use the **Sidebar Navigation** on the left to seamlessly explore and interact with my live application systems.")
st.markdown("---")

# Portfolio Cards Layout
st.subheader("📁 Showcase Catalog")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="project-card">
        <h4>📊 Page 1: Executive Dashboard</h4>
        <p style='color: #94A3B8; font-size: 14px;'>
        <b>Management & UI Focus:</b> Transforms chaotic multi-region business datasets into interactive, dark-mode optimized corporate visual command centers.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="project-card">
        <h4>🚨 Page 2: Automated Risk Tracker</h4>
        <p style='color: #94A3B8; font-size: 14px;'>
        <b>System Integrity Focus:</b> Demonstrates an automated Early Warning System (EWS) utilizing advanced anomaly tracking and real-time variance alerts.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="project-card">
        <h4>🔮 Page 3: Advanced BI Predictor</h4>
        <p style='color: #94A3B8; font-size: 14px;'>
        <b>Predictive Analytics:</b> Features algorithmic sales forecasting alongside user velocity engines and data diagnostic matrices.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.info("💡 **How to test:** Click on any system engine in the sidebar to run the application containers with dynamic dataset inputs.")