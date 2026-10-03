#!/usr/bin/env python3
"""
Script: 08_visualize_dyads.py
Description: Generates an FA-weighted RGB directional map using primary dyads 
             from bedpostx to verify fiber vector orientation field.
"""

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

RAW_DIR = "data/raw"
BPX_DIR = "data/bedpostx_input.bedpostX"
FA_PATH = os.path.join(RAW_DIR, "dti_FA.nii.gz")
DYADS_PATH = os.path.join(BPX_DIR, "dyads1.nii.gz")
OUT_QA = os.path.join(RAW_DIR, "qa_dyads_rgb.png")

def main():
    print("=== [DAY 12] Fiber Vector (Dyads) RGB Visualization ===")

    # 1. Validate files
    for path in [FA_PATH, DYADS_PATH]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing required file: {path}")

    # 2. Load volumes
    fa_img = nib.load(FA_PATH)
    dyads_img = nib.load(DYADS_PATH)

    fa_data = fa_img.get_fdata()
    dyads_data = dyads_img.get_fdata()

    # 3. Create FA-modulated RGB map: RGB = |Vector| * FA
    rgb_map = np.abs(dyads_data)
    for c in range(3):
        rgb_map[..., c] *= fa_data

    rgb_map = np.clip(rgb_map, 0, 1)

    # 4. Extract middle slice for display
    mid_slice = fa_data.shape[2] // 2
    rgb_slice = np.rot90(rgb_map[:, :, mid_slice, :])

    # 5. Plot and save
    plt.figure(figsize=(6, 6))
    plt.imshow(rgb_slice)
    plt.title("FA-Weighted Primary Direction Map (Dyads1 RGB)")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(OUT_QA, dpi=150)
    plt.close()

    print(f"[✓] RGB Dyad QA image successfully saved to: {OUT_QA}")
    print("=== [SUCCESS] Day 12 Dyad QA Complete! ===")

if __name__ == "__main__":
    main()
