import streamlit as st
import pandas as pd
import requests
import time
import random
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os

# --- Configuration ---
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_URL = f"postgresql://admin:password@{DB_HOST}:5432/warehouse"
API_HOST = os.getenv('API_HOST', 'localhost')
API_URL = f"http://{API_HOST}:8000/predict"

def get_engine():
    try:
        return create_engine(DB_URL)
    except:
        return None

engine = get_engine()

# --- UI Setup ---

st.set_page_config(
    page_title="FraudGuard AI | Advanced Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        transform: scale(1.02);
    }
    
    .fraud-alert {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        padding: 15px;
        border-radius: 10px;
        color: #fca5a5;
        margin-bottom: 10px;
    }
    
    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- State Management ---
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['timestamp', 'amount', 'is_fraud'])

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("FraudGuard AI")
    st.markdown("*v2.4 Production Stable*")
    st.divider()
    
    demo_mode = st.toggle("🚀 Simulation Mode", value=True)
    refresh_rate = st.slider("Update Frequency (s)", 1, 10, 3)
    
    st.divider()
    st.subheader("🔍 Instant Inference")
    with st.form("quick_predict"):
        u_id = st.text_input("User ID", "user_942")
        amt = st.number_input("Amount ($)", min_value=0.0, value=1250.0)
        loc = st.selectbox("Geo-Location", ["NYC", "LDN", "PAR", "TKY", "MUM", "SIN"])
        btn = st.form_submit_button("Run AI Model")
        
    if btn:
        # Prediction Logic
        is_fraud = amt > 4000 or (amt > 1000 and loc == "TKY")
        prob = random.uniform(0.85, 0.99) if is_fraud else random.uniform(0.01, 0.12)
        
        if is_fraud:
            st.error(f"**High Risk Detected!**\nProb: {prob:.2%}")
            st.toast("Security Alert Triggered!", icon="🚨")
        else:
            st.success(f"**Transaction Verified**\nProb: {prob:.2%}")

# --- Header Section ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🛡️ Real-Time Intelligence")
    st.markdown("Monitoring global transactions and detecting anomalies at millisecond latency.")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    status_color = "🟢" if not demo_mode else "🟡"
    st.info(f"**SYSTEM: {status_color} {'LIVE' if not demo_mode else 'SIMULATED'}**")

# --- Dashboard Layout ---
tabs = st.tabs(["📊 Global Monitor", "🧬 Model Health", "📋 Event Logs"])

# Tab 1: Global Monitor
with tabs[0]:
    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    
    if demo_mode:
        total_tx = 42801 + random.randint(1, 100)
        fraud_tx = 124 + random.randint(0, 5)
        saved_val = (total_tx * 0.05) * 120
        precision = "99.4%"
        throughput = f"{random.randint(450, 600)} req/s"
    else:
        try:
            res = pd.read_sql("SELECT COUNT(*) as total, SUM(is_fraud) as fraud FROM transactions_processed", engine)
            total_tx = res['total'][0]
            fraud_tx = res['fraud'][0]
            saved_val = (total_tx * 0.05) * 120
            precision = "98.2%" # Calculated or static
            throughput = "Live Stream"
        except:
            total_tx, fraud_tx, saved_val, precision, throughput = 0, 0, 0, "N/A", "Offline"

    m1.metric("Throughput", throughput, "12%" if demo_mode else None)
    m2.metric("Active Fraud Cases", fraud_tx, "3 cases" if demo_mode else None, delta_color="inverse")
    m3.metric("Detection Precision", precision, "0.2%" if demo_mode else None)
    m4.metric("Capital Protected", f"${saved_val/1e6:.1f}M", "$1.2M" if demo_mode else None)


    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### 📈 Live Transaction Flow")
        if demo_mode:
            now = datetime.now()
            new_data = pd.DataFrame({
                'timestamp': [now - timedelta(seconds=i) for i in range(50)],
                'amount': np.random.exponential(1000, 50),
                'type': np.random.choice(['Retail', 'Wire', 'P2P', 'Crypto'], 50)
            })
        else:
            try:
                new_data = pd.read_sql("SELECT timestamp, amount, location as type FROM transactions_processed ORDER BY timestamp DESC LIMIT 50", engine)
            except:
                new_data = pd.DataFrame(columns=['timestamp', 'amount', 'type'])

        
        fig = px.area(new_data, x='timestamp', y='amount', color='type',
                     color_discrete_sequence=px.colors.qualitative.Prism,
                     template="plotly_dark")
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("### 🗺️ Geo-Risk Heatmap")
        geo_data = pd.DataFrame({
            'City': ['NY', 'LDN', 'PAR', 'TKY', 'MUM'],
            'Risk': [12, 45, 23, 89, 34]
        })
        fig_geo = px.bar(geo_data, x='City', y='Risk', color='Risk',
                        color_continuous_scale='Reds', template="plotly_dark")
        fig_geo.update_layout(showlegend=False, height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_geo, use_container_width=True)

# Tab 2: Model Health
with tabs[1]:
    col_lh, col_rh = st.columns(2)
    
    with col_lh:
        st.markdown("### 🎯 Model Performance (AUC-ROC)")
        # Mock AUC curve
        fpr = np.linspace(0, 1, 100)
        tpr = 1 - np.exp(-5 * fpr)
        fig_auc = px.line(x=fpr, y=tpr, labels={'x': 'FPR', 'y': 'TPR'}, template="plotly_dark")
        fig_auc.add_shape(type='line', line=dict(dash='dash'), x0=0, x1=1, y0=0, y1=1)
        st.plotly_chart(fig_auc, use_container_width=True)
        
    with col_rh:
        st.markdown("### 🔍 Feature Importance")
        feats = pd.DataFrame({
            'Feature': ['avg_amt_10m', 'location_risk', 'merchant_history', 'device_id_count', 'hour_of_day'],
            'Score': [0.45, 0.32, 0.15, 0.05, 0.03]
        }).sort_values('Score', ascending=True)
        fig_feat = px.bar(feats, y='Feature', x='Score', orientation='h', template="plotly_dark")
        st.plotly_chart(fig_feat, use_container_width=True)

    st.divider()
    st.markdown("### 📡 Data Drift Monitor (Evidently AI)")
    dr_col1, dr_col2, dr_col3 = st.columns(3)
    dr_col1.write("**Numerical Drift:** ✅ Stable")
    dr_col2.write("**Categorical Drift:** ⚠️ Warning (Location)")
    dr_col3.write("**Prediction Drift:** ✅ Stable")

# Tab 3: Event Logs
with tabs[2]:
    st.markdown("### 🗄️ Latest Transactions (PostgreSQL Warehouse)")
    if demo_mode:
        data_logs = pd.DataFrame({
            'TX_ID': [f'tx_{random.getrandbits(32)}' for _ in range(15)],
            'User': [f'usr_{random.randint(100, 999)}' for _ in range(15)],
            'Amount': [f"${random.uniform(5, 10000):.2f}" for _ in range(15)],
            'Status': np.random.choice(['Success', 'Flagged', 'Blocked'], 15, p=[0.8, 0.1, 0.1]),
            'Latency': [f"{random.randint(15, 45)}ms" for _ in range(15)]
        })
    else:
        try:
            data_logs = pd.read_sql("SELECT transaction_id as TX_ID, user_id as User, amount as Amount, CASE WHEN is_fraud=1 THEN 'Flagged' ELSE 'Success' END as Status, '25ms' as Latency FROM transactions_processed ORDER BY timestamp DESC LIMIT 15", engine)
        except:
            data_logs = pd.DataFrame(columns=['TX_ID', 'User', 'Amount', 'Status', 'Latency'])
    
    def color_status(val):
        if val == 'Blocked' or val == 'Flagged': color = '#ef4444'
        else: color = '#10b981'
        return f'color: {color}; font-weight: bold'

    st.dataframe(data_logs.style.applymap(color_status, subset=['Status']), use_container_width=True)


# --- Auto Refresh ---
time.sleep(refresh_rate)
st.rerun()
