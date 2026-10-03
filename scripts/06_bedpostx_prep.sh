#!/bin/bash
# ==============================================================================
# Script: 06_bedpostx_prep.sh
# Description: Sets up the standard input directory structure required for 
#              FSL bedpostx probabilistic fiber tracking.
# ==============================================================================

set -e  # Exit on error

RAW_DIR="data/raw"
BPX_DIR="data/bedpostx_input"

echo "=== [DAY 10] BEDPOSTX Input Directory Setup ==="

# 1. Create bedpostx input directory
mkdir -p "$BPX_DIR"

# 2. Verify preprocessed files exist
if [ ! -f "${RAW_DIR}/data_eddy.nii.gz" ] || [ ! -f "${RAW_DIR}/nodif_brain_mask.nii.gz" ]; then
    echo "ERROR: Missing preprocessed data_eddy.nii.gz or brain mask!"
    exit 1
fi

# 3. Copy/Link files to standard BEDPOSTX naming conventions
echo "[i] Staging dataset for BEDPOSTX..."
cp "${RAW_DIR}/data_eddy.nii.gz" "${BPX_DIR}/data.nii.gz"
cp "${RAW_DIR}/nodif_brain_mask.nii.gz" "${BPX_DIR}/nodif_brain_mask.nii.gz"
cp "${RAW_DIR}/bvals" "${BPX_DIR}/bvals"
cp "${RAW_DIR}/bvecs" "${BPX_DIR}/bvecs"

# 4. Confirm structure integrity
echo "[i] Checking BEDPOSTX input directory contents:"
ls -lh "$BPX_DIR"

if [ -f "${BPX_DIR}/data.nii.gz" ] && [ -f "${BPX_DIR}/nodif_brain_mask.nii.gz" ]; then
    echo "[✓] BEDPOSTX directory successfully initialized at: $BPX_DIR"
else
    echo "ERROR: BEDPOSTX staging failed!"
    exit 1
fi

echo "=== [SUCCESS] Day 10 Setup Completed! ==="
