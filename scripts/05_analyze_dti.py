#!/usr/bin/env python3
"""
Script: 05_analyze_dti.py
Description: Calculates summary statistics for FA and MD maps and generates
             a dual-panel visualization for pipeline QA.
"""

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

RAW_DIR = "data/raw"
FA_PATH = os.path.join(RAW_DIR, "dti_FA.nii.gz")
MD_PATH = os.path.join(RAW_DIR, "dti_MD.nii.gz")
MASK_PATH = os.path.join(RAW_DIR, "nodif_brain_mask.nii.gz")
OUT_QA = os.path.join(RAW_DIR, "qa_dti_maps.png")

def main():
    print("=== [DAY 9] DTI Metric Analysis & QA Visualization ===")

    # 1. Load volumes
    for path in [FA_PATH, MD_PATH, MASK_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required file: {path}")

    fa_img = nib.load(FA_PATH)
    md_img = nib.load(MD_PATH)
    mask_img = nib.load(MASK_PATH)

    fa_data = fa_img.get_fdata()
    md_data = md_img.get_fdata()
    mask_data = mask_img.get_fdata() > 0

    # 2. Compute non-zero brain mask statistics
    fa_brain = fa_data[mask_data]
    md_brain = md_data[mask_data]

    print(f"[i] Brain Voxels Count: {fa_brain.size}")
    print(f"[✓] FA Mean ± Std : {np.mean(fa_brain):.4f} ± {np.std(fa_brain):.4f}")
    print(f"[✓] MD Mean ± Std : {np.mean(md_brain):.6f} ± {np.std(md_brain):.6f}")

    # 3. Pick middle axial slice for visualization
    mid_slice = fa_data.shape[2] // 2

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    
    im0 = axes[0].imshow(fa_data[:, :, mid_slice], cmap="gray", origin="lower", vmin=0, vmax=1)
    axes[0].set_title("Fractional Anisotropy (FA)")
    axes[0].axis("off")
    fig.colorbar(im0, ax=axes[0], fraction=0.046, pad=0.04)

    im1 = axes[1].imshow(md_data[:, :, mid_slice], cmap="inferno", origin="lower")
    axes[1].set_title("Mean Diffusivity (MD)")
    axes[1].axis("off")
    fig.colorbar(im1, ax=axes[1], fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.savefig(OUT_QA, dpi=150)
    plt.close()

    print(f"[✓] DTI QA image saved to: {OUT_QA}")
    print("=== [SUCCESS] Day 9 Analysis Complete! ===")

if __name__ == "__main__":
    main()
