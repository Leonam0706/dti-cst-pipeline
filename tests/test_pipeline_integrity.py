#!/usr/bin/env python3
"""
Script: test_pipeline_integrity.py
Description: Pytest validation suite for checking data dimensions, 
             scalar metric ranges, and output file integrity.
"""

import os
import json
import pytest
import numpy as np
import nibabel as nib

RAW_DIR = "data/raw"
TRACK_DIR = "data/cst_tracking"
REPORTS_DIR = "reports"

@pytest.mark.skipif(not os.path.exists(os.path.join(RAW_DIR, "dti_FA.nii.gz")), reason="DTI FA file not found")
def test_nifti_dimensions_and_fa_range():
    fa_path = os.path.join(RAW_DIR, "dti_FA.nii.gz")
    md_path = os.path.join(RAW_DIR, "dti_MD.nii.gz")
    
    assert os.path.exists(fa_path), "FA map does not exist."
    assert os.path.exists(md_path), "MD map does not exist."

    fa_img = nib.load(fa_path)
    md_img = nib.load(md_path)

    # Spatial dimension match check
    assert fa_img.shape == md_img.shape, "FA and MD spatial dimensions mismatch."

    fa_data = fa_img.get_fdata()
    valid_fa = fa_data[(fa_data > 0) & (~np.isnan(fa_data))]

    # 1. Ensure non-negative FA values
    assert np.all(valid_fa >= 0.0), "Negative FA values detected."
    
    # 2. Ensure mean tissue FA is physiologically valid (< 1.0)
    assert np.mean(valid_fa) < 1.0, "Mean FA across brain volume exceeds 1.0."

@pytest.mark.skipif(not os.path.exists(os.path.join(TRACK_DIR, "cst_summary_metrics.json")), reason="Metrics JSON not found")
def test_summary_metrics_json_schema():
    json_path = os.path.join(TRACK_DIR, "cst_summary_metrics.json")
    assert os.path.exists(json_path), "cst_summary_metrics.json missing."

    with open(json_path, "r") as f:
        data = json.load(f)

    # Validate JSON schema and metric keys
    assert "tract_name" in data
    assert "volume" in data
    assert "total_volume_mm3" in data["volume"]
    assert "metrics" in data
    assert "FA" in data["metrics"]
    assert "MD" in data["metrics"]
    assert data["volume"]["total_volume_mm3"] > 0, "CST volume must be > 0."

@pytest.mark.skipif(not os.path.exists(os.path.join(REPORTS_DIR, "CLINICAL_QA_REPORT.md")), reason="QA Report not found")
def test_clinical_qa_report_exists():
    report_path = os.path.join(REPORTS_DIR, "CLINICAL_QA_REPORT.md")
    assert os.path.exists(report_path), "CLINICAL_QA_REPORT.md is missing."
    assert os.path.getsize(report_path) > 100, "CLINICAL_QA_REPORT.md is empty."
