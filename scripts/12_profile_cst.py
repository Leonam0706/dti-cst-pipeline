#!/usr/bin/env python3
"""
Script: 12_profile_cst.py
Description: Computes along-tract microstructural profiles (FA & MD per axial slice)
             along the reconstructed CST and generates a profile plot.
"""

import os
import numpy as np
import pandas as pd
import nibabel as nib
import matplotlib.pyplot as plt

RAW_DIR = "data/raw"
TRACK_DIR = "data/cst_tracking"

FA_PATH = os.path.join(RAW_DIR, "dti_FA.nii.gz")
MD_PATH = os.path.join(RAW_DIR, "dti_MD.nii.gz")
CST_MASK_PATH = os.path.join(TRACK_DIR, "cst_mask_thr05.nii.gz")

OUT_CSV = os.path.join(TRACK_DIR, "cst_profile_metrics.csv")
OUT_QA = os.path.join(TRACK_DIR, "qa_cst_profile.png")

def main():
    print("=== [DAY 16] Along-Tract CST Microstructural Profiling ===")

    # 1. Validate input files
    for path in [FA_PATH, MD_PATH, CST_MASK_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required file: {path}")

    # 2. Load volumes
    fa_data = nib.load(FA_PATH).get_fdata()
    md_data = nib.load(MD_PATH).get_fdata()
    cst_mask = nib.load(CST_MASK_PATH).get_fdata() > 0

    num_slices = fa_data.shape[2]
    slices, fa_means, fa_stds, md_means, md_stds = [], [], [], [], []

    # 3. Extract metrics per axial slice
    for z in range(num_slices):
        slice_mask = cst_mask[:, :, z]
        if np.any(slice_mask):
            fa_vals = fa_data[:, :, z][slice_mask]
            md_vals = md_data[:, :, z][slice_mask]

            slices.append(z)
            fa_means.append(np.mean(fa_vals))
            fa_stds.append(np.std(fa_vals))
            md_means.append(np.mean(md_vals))
            md_stds.append(np.std(md_vals))

    if not slices:
        raise ValueError("CST mask has no positive voxels to profile!")

    # 4. Save to CSV
    df = pd.DataFrame({
        "axial_slice": slices,
        "fa_mean": fa_means,
        "fa_std": fa_stds,
        "md_mean": md_means,
        "md_std": md_stds
    })
    df.to_csv(OUT_CSV, index=False)
    print(f"[✓] Saved along-tract CSV metrics to: {OUT_CSV}")

    # 5. Generate QA Profile Plot
    fig, ax1 = plt.subplots(figsize=(8, 5))

    color = "tab:blue"
    ax1.set_xlabel("Axial Slice (Inferior -> Superior)")
    ax1.set_ylabel("Fractional Anisotropy (FA)", color=color)
    ax1.plot(slices, fa_means, color=color, marker="o", linewidth=2, label="FA")
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()
    color = "tab:red"
    ax2.set_ylabel("Mean Diffusivity (MD)", color=color)
    ax2.plot(slices, md_means, color=color, marker="s", linestyle="--", linewidth=2, label="MD")
    ax2.tick_params(axis="y", labelcolor=color)

    plt.title("Along-Tract CST Microstructural Profile")
    fig.tight_layout()
    plt.savefig(OUT_QA, dpi=150)
    plt.close()

    print(f"[✓] Profile plot saved to: {OUT_QA}")
    print("=== [SUCCESS] Day 16 Along-Tract Profiling Completed! ===")

if __name__ == "__main__":
    main()
