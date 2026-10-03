#!/usr/bin/env python3
"""
Script: 14_extract_cst_metrics.py
Description: Computes whole-tract quantitative summary statistics (Volume, FA, MD, AD, RD)
             for the thresholded CST mask and exports to JSON.
"""

import os
import json
import numpy as np
import nibabel as nib

RAW_DIR = "data/raw"
TRACK_DIR = "data/cst_tracking"

CST_MASK_PATH = os.path.join(TRACK_DIR, "cst_mask_thr05.nii.gz")
FA_PATH = os.path.join(RAW_DIR, "dti_FA.nii.gz")
MD_PATH = os.path.join(RAW_DIR, "dti_MD.nii.gz")
L1_PATH = os.path.join(RAW_DIR, "dti_L1.nii.gz")
L2_PATH = os.path.join(RAW_DIR, "dti_L2.nii.gz")
L3_PATH = os.path.join(RAW_DIR, "dti_L3.nii.gz")

OUT_JSON = os.path.join(TRACK_DIR, "cst_summary_metrics.json")

def get_stats(data, mask):
    vals = data[mask]
    return {
        "mean": float(np.mean(vals)),
        "std": float(np.std(vals)),
        "median": float(np.median(vals)),
        "iqr": float(np.percentile(vals, 75) - np.percentile(vals, 25))
    }

def main():
    print("=== [DAY 18] Whole-Tract CST Quantitative Metrics Extraction ===")

    # 1. Check required inputs
    required_files = [CST_MASK_PATH, FA_PATH, MD_PATH, L1_PATH, L2_PATH, L3_PATH]
    for path in required_files:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required file: {path}")

    # 2. Load volumes
    mask_img = nib.load(CST_MASK_PATH)
    mask = mask_img.get_fdata() > 0

    voxel_zooms = mask_img.header.get_zooms()[:3]
    voxel_volume_mm3 = float(np.prod(voxel_zooms))
    voxel_count = int(np.sum(mask))
    total_volume_mm3 = float(voxel_count * voxel_volume_mm3)

    fa_data = nib.load(FA_PATH).get_fdata()
    md_data = nib.load(MD_PATH).get_fdata()
    l1_data = nib.load(L1_PATH).get_fdata()
    l2_data = nib.load(L2_PATH).get_fdata()
    l3_data = nib.load(L3_PATH).get_fdata()

    # Calculate Radial Diffusivity (RD) = (L2 + L3) / 2
    rd_data = (l2_data + l3_data) / 2.0

    # 3. Compile Summary Statistics
    summary = {
        "tract_name": "Left Corticospinal Tract (CST)",
        "threshold": "5% waytotal probability density",
        "volume": {
            "voxel_count": voxel_count,
            "voxel_size_mm3": voxel_zooms,
            "total_volume_mm3": round(total_volume_mm3, 2)
        },
        "metrics": {
            "FA": get_stats(fa_data, mask),
            "MD": get_stats(md_data, mask),
            "AD_L1": get_stats(l1_data, mask),
            "RD": get_stats(rd_data, mask)
        }
    }

    # 4. Save to JSON
    with open(OUT_JSON, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"[✓] Quantitative summary metrics saved: {OUT_JSON}")
    print(f"[i] CST Volume: {total_volume_mm3:.2f} mm³ ({voxel_count} voxels)")
    print(f"[i] Mean FA: {summary['metrics']['FA']['mean']:.4f} ± {summary['metrics']['FA']['std']:.4f}")
    print(f"[i] Mean MD: {summary['metrics']['MD']['mean']:.6f} ± {summary['metrics']['MD']['std']:.6f}")
    print("=== [SUCCESS] Day 18 Quantitative Extraction Completed! ===")

if __name__ == "__main__":
    main()
