#!/usr/bin/env python3
"""
Script: 11_threshold_cst.py
Description: Normalizes raw fdt_paths by waytotal and applies probability 
             thresholding to generate a clean binary CST tract mask.
"""

import os
import numpy as np
import nibabel as nib

TRACK_DIR = "data/cst_tracking"
FDT_PATH = os.path.join(TRACK_DIR, "fdt_paths.nii.gz")
WAYTOTAL_PATH = os.path.join(TRACK_DIR, "waytotal")
OUT_NORM = os.path.join(TRACK_DIR, "cst_normalized.nii.gz")
OUT_MASK = os.path.join(TRACK_DIR, "cst_mask_thr05.nii.gz")

# Probability threshold (5% of valid waytotal pathways)
THRESHOLD = 0.05

def main():
    print("=== [DAY 15] CST Streamline Density Thresholding ===")

    # 1. Load inputs
    if not os.path.exists(FDT_PATH) or not os.path.exists(WAYTOTAL_PATH):
        raise FileNotFoundError("Missing required probtrackx2 output files!")

    fdt_img = nib.load(FDT_PATH)
    fdt_data = fdt_img.get_fdata()

    with open(WAYTOTAL_PATH, "r") as f:
        waytotal = float(f.read().strip())

    print(f"[i] Total valid streamlines (waytotal): {int(waytotal)}")

    # 2. Normalize by waytotal
    norm_data = fdt_data / waytotal
    norm_img = nib.Nifti1Image(norm_data, fdt_img.affine, fdt_img.header)
    nib.save(norm_img, OUT_NORM)
    print(f"[✓] Saved normalized probability map: {OUT_NORM}")

    # 3. Apply thresholding (e.g., top 5% relative probability density)
    binary_mask = (norm_data >= THRESHOLD).astype(np.uint8)
    tract_voxels = np.sum(binary_mask)
    
    mask_img = nib.Nifti1Image(binary_mask, fdt_img.affine, fdt_img.header)
    nib.save(mask_img, OUT_MASK)

    print(f"[✓] Thresholded CST mask saved: {OUT_MASK}")
    print(f"[✓] Retained CST Tract Volume: {tract_voxels} voxels (threshold >= {THRESHOLD})")
    print("=== [SUCCESS] Day 15 Thresholding Complete! ===")

if __name__ == "__main__":
    main()
