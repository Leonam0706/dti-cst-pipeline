#!/bin/bash
# ==============================================================================
# Script: 07_run_bedpostx.sh
# Description: Executes FSL bedpostx on staged dMRI data to build 
#              multi-fiber orientation distribution functions (fODFs).
# ==============================================================================

set -e  # Exit on error

BPX_DIR="data/bedpostx_input"
BPX_OUT="data/bedpostx_input.bedpostX"

echo "=== [DAY 11] Running BEDPOSTX Fiber Orientation Estimation ==="

# 1. Verify input directory exists
if [ ! -d "$BPX_DIR" ]; then
    echo "ERROR: Input directory $BPX_DIR does not exist. Run 06_bedpostx_prep.sh first."
    exit 1
fi

# 2. Run bedpostx (using 2 fibers per voxel -n 2, compressed MCMC sampling for speed)
# Note: On synthetic/test datasets, bedpostx processes quickly.
echo "[i] Launching bedpostx (this estimates stick fraction and fiber orientation)..."
bedpostx "$BPX_DIR" -n 2 --model=1

# 3. Verify output directory and primary dyad creation
if [ -d "$BPX_OUT" ] && [ -f "${BPX_OUT}/dyads1.nii.gz" ]; then
    echo "[✓] BEDPOSTX successfully completed!"
    echo "[✓] Output directory populated: $BPX_OUT"
else
    echo "ERROR: BEDPOSTX output validation failed!"
    exit 1
fi

echo "=== [SUCCESS] Day 11 BEDPOSTX Execution Completed! ==="
