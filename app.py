import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Agri-Environmental Mitigation Engine", layout="wide")

st.title("Serverless Catchment Decision Support")
st.caption("Real-Time Spatiotemporal Monitoring of Land-Water Interactions & Nutrient Leaching")

st.sidebar.header("Catchment Configuration")
selected_zone = st.sidebar.selectbox("Target Agricultural Catchment", ["Canterbury Plains (Nitrate Focus)", "Waikato Basin (Sediment/Dairy)", "Southland Catchment (Phosphorus)"])
weather_shock = st.sidebar.slider("Simulate Extreme Precipitation Event", 1.0, 5.0, 3.0)
run_simulation = st.sidebar.button("Initialize ML Mitigation Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: IoT Telemetry -> AWS Normalization -> XGBoost Runoff Inference")

if run_simulation:
    st.subheader(f"Active Environmental Monitor: {selected_zone}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_rain = col1.empty()
    metric_leaching = col2.empty()
    metric_quality = col3.empty()
    metric_status = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(3434)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    nutrient_runoff = []
    water_quality_index = []
    
    base_runoff = 15.0 
    base_quality = 95.0
    
    for i in range(100):
        if i < 30:
            current_rain = np.random.uniform(0.0, 2.0)
            current_runoff = base_runoff + np.random.uniform(-1.0, 2.0)
            current_quality = base_quality + np.random.uniform(-1.0, 1.0)
            status = "OPTIMAL BASELINE"
        elif i >= 30 and i < 65:
            current_rain = (i - 30) * (5.0 * weather_shock) + np.random.uniform(-5.0, 10.0)
            current_runoff = base_runoff + (current_rain * 0.8) + np.random.uniform(-2.0, 5.0)
            current_quality = base_quality - (current_runoff * 0.3) + np.random.uniform(-2.0, 2.0)
            status = "CRITICAL LEACHING DETECTED"
        else:
            current_rain = max(0.0, current_rain - np.random.uniform(5.0, 15.0))
            current_runoff = max(base_runoff, current_runoff - np.random.uniform(2.0, 8.0))
            current_quality = min(98.0, current_quality + np.random.uniform(1.0, 4.0))
            status = "MITIGATION PROTOCOLS ACTIVE"
            
        current_quality = max(0.0, current_quality)
            
        nutrient_runoff.append(current_runoff)
        water_quality_index.append(current_quality)
        
        metric_rain.metric("Precipitation Intensity", f"{current_rain:.1f} mm/hr")
        metric_leaching.metric("Nutrient Runoff (kg/ha)", f"{current_runoff:.1f}", f"+{(current_runoff - base_runoff):.1f} Variance")
        metric_quality.metric("Catchment Water Quality Index", f"{current_quality:.1f} pts")
        
        if status == "CRITICAL LEACHING DETECTED":
            metric_status.metric("Decision Support System", status, "Triggering Advisories")
        elif status == "MITIGATION PROTOCOLS ACTIVE":
            metric_status.metric("Decision Support System", status, "Recovering")
        else:
            metric_status.metric("Decision Support System", status, "Stable")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=nutrient_runoff, mode='lines', name='Nutrient Leaching (kg/ha)', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=water_quality_index, mode='lines', name='Water Quality Index', yaxis='y2', line=dict(color='blue', dash='dot')))
        
        fig.update_layout(
            title="Agri-Environmental Mitigation: Nutrient Leaching vs Catchment Water Quality",
            xaxis=dict(title="High-Frequency Temporal Baseline"),
            yaxis=dict(title="Nutrient Runoff (kg/ha)"),
            yaxis2=dict(title="Water Quality Index", overlaying='y', side='right', range=[0, 100]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if status == "CRITICAL LEACHING DETECTED" and i == 35:
            log_placeholder.error(f"ENVIRONMENTAL ALERT: Severe precipitation triggering massive nutrient runoff detected at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine instantly calculating spatial mitigation advisories for vulnerable farm nodes.")
        elif status == "MITIGATION PROTOCOLS ACTIVE" and i == 65:
            log_placeholder.warning(f"ORCHESTRATION SUCCESS: Cloud-native decision support system deployed farm-level interventions. Soil saturation stabilizing. Catchment water quality recovering to baseline.")
        elif status == "OPTIMAL BASELINE" and i % 5 == 0:
            log_placeholder.success(f"Log: Telemetry tick {i} ingested via serverless middleware. Land-water interactions operating within sustainable regulatory parameters.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The serverless cloud pipeline successfully scaled agricultural decision support, mitigating catchment water quality degradation in real-time.")
else:
    st.info("Click 'Initialize ML Mitigation Engine' in the sidebar to simulate high-frequency agri-environmental data ingestion.")