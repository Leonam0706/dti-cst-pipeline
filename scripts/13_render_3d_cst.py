#!/usr/bin/env python3
"""
Script: 13_render_3d_cst.py
Description: Generates a multi-planar (Axial, Coronal, Sagittal) quality assurance
             overlay of the reconstructed CST tract on the background FA map.
"""

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

RAW_DIR = "data/raw"
TRACK_DIR = "data/cst_tracking"

FA_PATH = os.path.join(RAW_DIR, "dti_FA.nii.gz")
CST_MASK_PATH = os.path.join(TRACK_DIR, "cst_mask_thr05.nii.gz")
OUT_QA = os.path.join(TRACK_DIR, "qa_cst_3d_overlay.png")

def main():
    print("=== [DAY 17] Multi-Planar CST Overlay Rendering ===")

    # 1. Check input files
    for path in [FA_PATH, CST_MASK_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required file: {path}")

    # 2. Load FA and CST mask
    fa_img = nib.load(FA_PATH)
    cst_img = nib.load(CST_MASK_PATH)

    fa_data = fa_img.get_fdata()
    cst_data = cst_img.get_fdata() > 0

    # 3. Determine slice centers based on CST mask bounding box
    indices = np.argwhere(cst_data)
    if indices.size == 0:
        raise ValueError("CST mask is empty! Check thresholding output.")

    x_mid, y_mid, z_mid = np.mean(indices, axis=0).astype(int)

    # 4. Extract slices
    sag_fa = np.rot90(fa_data[x_mid, :, :])
    sag_cst = np.rot90(cst_data[x_mid, :, :])

    cor_fa = np.rot90(fa_data[:, y_mid, :])
    cor_cst = np.rot90(cst_data[:, y_mid, :])

    axi_fa = np.rot90(fa_data[:, :, z_mid])
    axi_cst = np.rot90(cst_data[:, :, z_mid])

    # 5. Render 3-panel figure
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Sagittal View
    axes[0].imshow(sag_fa, cmap="gray", origin="lower")
    axes[0].imshow(np.ma.masked_where(~sag_cst, sag_cst), cmap="autumn", alpha=0.8, origin="lower")
    axes[0].set_title(f"Sagittal (X={x_mid})")
    axes[0].axis("off")

    # Coronal View
    axes[1].imshow(cor_fa, cmap="gray", origin="lower")
    axes[1].imshow(np.ma.masked_where(~cor_cst, cor_cst), cmap="autumn", alpha=0.8, origin="lower")
    axes[1].set_title(f"Coronal (Y={y_mid})")
    axes[1].axis("off")

    # Axial View
    axes[2].imshow(axi_fa, cmap="gray", origin="lower")
    axes[2].imshow(np.ma.masked_where(~axi_cst, axi_cst), cmap="autumn", alpha=0.8, origin="lower")
    axes[2].set_title(f"Axial (Z={z_mid})")
    axes[2].axis("off")

    plt.suptitle("Corticospinal Tract (CST) Multi-Planar Overlay on FA Map", fontsize=14)
    plt.tight_layout()
    plt.savefig(OUT_QA, dpi=150)
    plt.close()

    print(f"[✓] Multi-planar overlay plot saved to: {OUT_QA}")
    print("=== [SUCCESS] Day 17 Visualization Rendering Completed! ===")

if __name__ == "__main__":
    main()
