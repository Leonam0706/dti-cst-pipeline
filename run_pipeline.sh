#!/bin/bash
# ==============================================================================
# Script: run_pipeline.sh
# Description: Master orchestrator script for the clinical dMRI-to-CST 
#              probabilistic tractography and microstructural profiling pipeline.
# ==============================================================================

set -e  # Exit immediately if any command fails

LOG_DIR="logs"
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/pipeline_execution_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -i "$LOG_FILE") 2>&1

echo "================================================================="
echo "  CLINICAL dMRI-TO-CST TRACTOGRAPHY PIPELINE (WSL2 / Ubuntu 24.04)"
echo "  Started at: $(date)"
echo "================================================================="

# --- Stage 1: Data Verification & Tensor Fitting ---
echo -e "\n[STAGE 1] Running Tensor Fitting & Microstructural Analysis..."
python3 scripts/05_analyze_dti.py

# --- Stage 2: ROI Generation ---
echo -e "\n[STAGE 2] Defining CST Seed, Waypoint, and Exclusion ROIs..."
python3 scripts/09_define_cst_rois.py

# --- Stage 3: Probabilistic Tractography ---
echo -e "\n[STAGE 3] Running Probabilistic Tractography (probtrackx2)..."
./scripts/10_run_probtrackx.sh

# --- Stage 4: Density Thresholding & Normalization ---
echo -e "\n[STAGE 4] Normalizing & Thresholding CST Density Map..."
python3 scripts/11_threshold_cst.py

# --- Stage 5: Microstructural Profiling & Visualization ---
echo -e "\n[STAGE 5] Profiling Along-Tract Metrics & Rendering Overlays..."
python3 scripts/12_profile_cst.py
python3 scripts/13_render_3d_cst.py

# --- Stage 6: Quantitative Extraction & QA Report Generation ---
echo -e "\n[STAGE 6] Extracting Metrics & Generating Clinical QA Report..."
python3 scripts/14_extract_cst_metrics.py
python3 scripts/15_generate_qa_report.py

echo -e "\n================================================================="
echo "  [SUCCESS] End-to-End CST Pipeline Completed Successfully!"
echo "  Finished at: $(date)"
echo "  Log File Saved To: ${LOG_FILE}"
echo "================================================================="
