#!/usr/bin/env python3
"""
Script: app.py
Description: Interactive Streamlit Dashboard for Clinical dMRI CST Tractography Portfolio.
"""

import os
import json
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="dMRI CST Tractography Showcase",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Clinical dMRI CST Probabilistic Tractography Pipeline")
st.markdown("""
**Automated End-to-End Processing & Microstructural Quantification of the Corticospinal Tract (CST)**
""")

# Sidebar Navigation
st.sidebar.header("Pipeline Navigation")
page = st.sidebar.radio("Select View:", ["Summary Dashboard", "Along-Tract Profiles", "QA & Metrics Report"])

# Load JSON Metrics
METRICS_PATH = "data/cst_tracking/cst_summary_metrics.json"
PROFILE_PATH = "reports/cst_profile_metrics.csv"

@st.cache_data
def load_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r") as f:
            return json.load(f)
    return None

@st.cache_data
def load_profile():
    if os.path.exists(PROFILE_PATH):
        return pd.read_csv(PROFILE_PATH)
    return None

metrics_data = load_metrics()
profile_df = load_profile()

if page == "Summary Dashboard":
    st.header("📊 Executive Metrics Summary")
    
    if metrics_data:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Tract Name", metrics_data.get("tract_name", "CST"))
        col2.metric("Tract Volume (mm³)", f"{metrics_data['volume']['total_volume_mm3']:.1f}")
        col3.metric("Mean FA", f"{metrics_data['metrics']['FA']['mean']:.3f}")
        col4.metric("Mean MD (mm²/s)", f"{metrics_data['metrics']['MD']['mean']:.2e}")
        
        st.markdown("---")
        st.subheader("Microstructural Metric Distribution")
        
        df_summary = pd.DataFrame({
            "Metric": ["Fractional Anisotropy (FA)", "Mean Diffusivity (MD)"],
            "Mean": [metrics_data['metrics']['FA']['mean'], metrics_data['metrics']['MD']['mean']],
            "Std Dev": [metrics_data['metrics']['FA']['std'], metrics_data['metrics']['MD']['std']],
            "Min": [metrics_data['metrics']['FA']['min'], metrics_data['metrics']['MD']['min']],
            "Max": [metrics_data['metrics']['FA']['max'], metrics_data['metrics']['MD']['max']]
        })
        st.dataframe(df_summary, use_container_width=True)
    else:
        st.warning("Metrics JSON file not found at `data/cst_tracking/cst_summary_metrics.json`.")

elif page == "Along-Tract Profiles":
    st.header("📈 CST Along-Tract Microstructural Profiling")
    
    if profile_df is not None:
        fig, ax1 = plt.subplots(figsize=(10, 4))
        
        ax1.set_xlabel("Tract Position (Inferior to Superior)")
        ax1.set_ylabel("Fractional Anisotropy (FA)", color="tab:blue")
        ax1.plot(profile_df["position"], profile_df["mean_fa"], color="tab:blue", label="Mean FA", linewidth=2)
        ax1.tick_params(axis="y", labelcolor="tab:blue")
        
        ax2 = ax1.twinx()
        ax2.set_ylabel("Mean Diffusivity (MD)", color="tab:red")
        ax2.plot(profile_df["position"], profile_df["mean_md"], color="tab:red", linestyle="--", label="Mean MD", linewidth=2)
        ax2.tick_params(axis="y", labelcolor="tab:red")
        
        plt.title("Along-Tract Profiles: FA and MD")
        fig.tight_layout()
        st.pyplot(fig)
        
        st.subheader("Raw Profile Data")
        st.dataframe(profile_df, use_container_width=True)
    else:
        st.warning("Along-tract profile CSV not found at `reports/cst_profile_metrics.csv`.")

elif page == "QA & Metrics Report":
    st.header("📋 Clinical QA & Integrity Report")
    
    REPORT_PATH = "reports/CLINICAL_QA_REPORT.md"
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            report_text = f.read()
        st.markdown(report_text)
    else:
        st.warning("Clinical QA Report not found at `reports/CLINICAL_QA_REPORT.md`.")
