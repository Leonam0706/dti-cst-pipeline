#!/usr/bin/env python3
"""
Script: 09_define_cst_rois.py
Description: Generates binary seed, waypoint, and exclusion ROI masks for 
             Corticospinal Tract (CST) probabilistic tractography.
"""

import os
import numpy as np
import nibabel as nib

RAW_DIR = "data/raw"
ROI_DIR = "data/rois"
MASK_PATH = os.path.join(RAW_DIR, "nodif_brain_mask.nii.gz")

os.makedirs(ROI_DIR, exist_ok=True)

def create_sphere_mask(shape, center, radius):
    """Creates a 3D binary sphere mask centered at given voxel coordinates."""
    x, y, z = np.ogrid[:shape[0], :shape[1], :shape[2]]
    dist_from_center = np.sqrt((x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2)
    return (dist_from_center <= radius).astype(np.uint8)

def main():
    print("=== [DAY 13] Defining CST Probabilistic Tracking ROIs ===")

    if not os.path.exists(MASK_PATH):
        raise FileNotFoundError(f"Missing brain mask: {MASK_PATH}")

    ref_img = nib.load(MASK_PATH)
    shape = ref_img.shape
    affine = ref_img.affine

    # Estimate center slice coordinates for test volume
    cx, cy, cz = shape[0] // 2, shape[1] // 2, shape[2] // 2

    # 1. Define Seed ROI (Peduncle level - lower brainstem)
    seed_center = (cx - 5, cy - 2, cz - 8)
    seed_data = create_sphere_mask(shape, seed_center, radius=3)
    seed_img = nib.Nifti1Image(seed_data, affine, ref_img.header)
    seed_path = os.path.join(ROI_DIR, "cst_seed_left.nii.gz")
    nib.save(seed_img, seed_path)
    print(f"[✓] Created Seed ROI: {seed_path}")

    # 2. Define Waypoint ROI (Internal Capsule / Motor Cortex)
    waypoint_center = (cx - 5, cy - 2, cz + 6)
    waypoint_data = create_sphere_mask(shape, waypoint_center, radius=4)
    waypoint_img = nib.Nifti1Image(waypoint_data, affine, ref_img.header)
    waypoint_path = os.path.join(ROI_DIR, "cst_waypoint_left.nii.gz")
    nib.save(waypoint_img, waypoint_path)
    print(f"[✓] Created Waypoint ROI: {waypoint_path}")

    # 3. Define Midline Exclusion Mask (Prevents contralateral crossing)
    excl_data = np.zeros(shape, dtype=np.uint8)
    excl_data[cx:, :, :] = 1  # Exclude right hemisphere for left CST tracking
    excl_img = nib.Nifti1Image(excl_data, affine, ref_img.header)
    excl_path = os.path.join(ROI_DIR, "cst_exclude_midline.nii.gz")
    nib.save(excl_img, excl_path)
    print(f"[✓] Created Exclusion Mask: {excl_path}")

    print("=== [SUCCESS] Day 13 ROI Generation Completed! ===")

if __name__ == "__main__":
    main()
