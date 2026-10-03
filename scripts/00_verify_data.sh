#!/bin/bash
# ==============================================================================
# Script: 00_verify_data.sh
# Description: Validates raw dMRI NIfTI volumes, bvals, and bvecs consistency.
# ==============================================================================

set -e  # Exit on error

RAW_DIR="data/raw"
DATA="${RAW_DIR}/data.nii.gz"
BVALS="${RAW_DIR}/bvals"
BVECS="${RAW_DIR}/bvecs"

echo "=== [DAY 4] Starting dMRI Data Integrity Verification ==="

# 1. Check File Existence
for file in "$DATA" "$BVALS" "$BVECS"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file $file not found!"
        exit 1
    fi
done
echo "[✓] All raw input files present."

# 2. Verify Volume Dimensions using FSL
DIM4=$(fslval "$DATA" dim4)
echo "[i] Number of 4D volumes in NIfTI: $DIM4"

# 3. Verify Gradient Count in bvals
BVAL_COUNT=$(wc -w < "$BVALS")
echo "[i] Total b-values counted: $BVAL_COUNT"

if [ "$DIM4" -ne "$BVAL_COUNT" ]; then
    echo "ERROR: Dimension mismatch! NIfTI volumes ($DIM4) != bvals count ($BVAL_COUNT)"
    exit 1
else
    echo "[✓] NIfTI 4D volumes match bvals count."
fi

# 4. Check bvecs rows/columns
BVEC_COUNT=$(wc -w < "$BVECS")
EXPECTED_BVEC=$(( BVAL_COUNT * 3 ))

if [ "$BVEC_COUNT" -ne "$EXPECTED_BVEC" ]; then
    echo "ERROR: bvecs matrix mismatch! Expected $EXPECTED_BVEC entries (3x$BVAL_COUNT), got $BVEC_COUNT"
    exit 1
else
    echo "[✓] bvecs matrix format is valid (3 x $BVAL_COUNT)."
fi

echo "=== [SUCCESS] Raw dMRI Dataset Verified Successfully! ==="
