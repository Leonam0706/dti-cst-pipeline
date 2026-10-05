# Clinical dMRI CST Tractography Pipeline Architecture

## System Overview

This repository provides an automated, production-grade end-to-end processing pipeline for clinical diffusion MRI (dMRI) data, specifically optimized for reconstructing the Left Corticospinal Tract (CST) and extracting microstructural metrics (FA, MD, AD, RD).

## Pipeline Workflow
## Directory Architecture
## Modular Scripts Summary

| Script Name | Purpose | Key Output |
| :--- | :--- | :--- |
| `05_analyze_dti.py` | Calculates DTI tensor metrics | `dti_FA.nii.gz`, `dti_MD.nii.gz`, `dti_L1.nii.gz` |
| `09_define_cst_rois.py` | Defines seed, waypoint, and exclusion ROIs | `cst_seed.nii.gz`, `cst_waypoint.nii.gz` |
| `10_run_probtrackx.sh` | Runs probabilistic tractography | `fdt_paths.nii.gz`, `waytotal` |
| `11_threshold_cst.py` | Applies 5% waytotal thresholding | `cst_mask_thr05.nii.gz` |
| `12_profile_cst.py` | Samples along-tract diffusion values | `cst_profile_metrics.csv`, `qa_cst_profile.png` |
| `13_render_3d_cst.py` | Generates multi-planar overlay plots | `qa_cst_3d_overlay.png` |
| `14_extract_cst_metrics.py` | Calculates whole-tract volume & metrics | `cst_summary_metrics.json` |
| `15_generate_qa_report.py` | Compiles QA summary report | `reports/CLINICAL_QA_REPORT.md` |
| `run_pipeline.sh` | End-to-end master orchestrator | Complete pipeline execution log |
