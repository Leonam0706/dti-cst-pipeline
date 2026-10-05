#!/usr/bin/env bash
# ==============================================================================
# Pipeline Master Orchestrator: Clinical dMRI CST Probabilistic Tractography
# ==============================================================================
set -euo pipefail

echo "================================================================="
echo " Starting Clinical dMRI CST Tractography Pipeline Execution "
echo "================================================================="

# Step 0: Data Verification
echo "[1/6] Running Data Verification & Visual QA Setup..."
bash scripts/00_verify_data.sh

# Step 1-2: Preprocessing & Brain Extraction
echo "[2/6] Executing Brain Extraction & Eddy Current Correction..."
bash scripts/02_brain_extraction.sh
bash scripts/03_eddy_correction.sh

# Step 3-4: DTI Fitting & Tensor Modeling
echo "[3/6] Fitting Diffusion Tensors (dtifit) & Bedpostx Modeling..."
bash scripts/04_dtifit.sh
bash scripts/06_bedpostx_prep.sh

# Step 5: Probabilistic Tractography
echo "[4/6] Defining CST ROIs & Running Probtrackx2..."
python3 scripts/09_define_cst_rois.py
bash scripts/10_run_probtrackx.sh

# Step 6: Post-processing, Metric Extraction & QA Reporting
echo "[5/6] Extracting CST Metrics & Profiling Along Tract..."
python3 scripts/11_threshold_cst.py
python3 scripts/12_profile_cst.py
python3 scripts/14_extract_cst_metrics.py

echo "[6/6] Generating Final Clinical QA Report..."
python3 scripts/15_generate_qa_report.py

echo "================================================================="
echo " Pipeline Execution Completed Successfully! "
echo " Clinical Report Generated at: reports/CLINICAL_QA_REPORT.md "
echo "================================================================="
