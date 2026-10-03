#!/bin/bash
# ==============================================================================
# Script: 04_dtifit.sh
# Description: Fits the diffusion tensor model using FSL dtifit to compute FA, MD, L1-3, V1-3.
# ==============================================================================

set -e  # Exit on error

RAW_DIR="data/raw"
DATA="${RAW_DIR}/data_eddy.nii.gz"
MASK="${RAW_DIR}/nodif_brain_mask.nii.gz"
BVALS="${RAW_DIR}/bvals"
BVECS="${RAW_DIR}/bvecs"
OUT_PREFIX="${RAW_DIR}/dti"

echo "=== [DAY 8] Starting Diffusion Tensor Fitting (dtifit) ==="

# 1. Verify required inputs exist
for FILE in "$DATA" "$MASK" "$BVALS" "$BVECS"; do
    if [ ! -f "$FILE" ]; then
        echo "ERROR: Required input file $FILE is missing!"
        exit 1
    fi
done

# 2. Run dtifit
echo "[i] Running dtifit model fitting..."
dtifit -k "$DATA" -m "$MASK" -r "$BVECS" -b "$BVALS" -o "$OUT_PREFIX" --save_tensor

# 3. Verify key DTI metric outputs
if [ -f "${OUT_PREFIX}_FA.nii.gz" ] && [ -f "${OUT_PREFIX}_MD.nii.gz" ]; then
    echo "[✓] dtifit successfully generated FA and MD maps!"
else
    echo "ERROR: dtifit execution failed!"
    exit 1
fi

echo "=== [SUCCESS] Day 8 Tensor Fitting Completed! ==="
