#!/bin/bash
# ==============================================================================
# Script: 10_run_probtrackx.sh
# Description: Executes FSL probtrackx2 to reconstruct the Left CST
#              using seed, waypoint, and exclusion masks.
# ==============================================================================

set -e  # Exit on error

BPX_DIR="data/bedpostx_input.bedpostX"
ROI_DIR="data/rois"
OUT_DIR="data/cst_tracking"

SEED="${ROI_DIR}/cst_seed_left.nii.gz"
WAYPOINT="${ROI_DIR}/cst_waypoint_left.nii.gz"
EXCLUDE="${ROI_DIR}/cst_exclude_midline.nii.gz"
MASK="${BPX_DIR}/nodif_brain_mask.nii.gz"

echo "=== [DAY 14] Running Probabilistic Tractography (probtrackx2) ==="

# 1. Check required input files
for FILE in "$SEED" "$WAYPOINT" "$EXCLUDE" "$MASK"; do
    if [ ! -f "$FILE" ]; then
        echo "ERROR: Required file $FILE missing!"
        exit 1
    fi
done

# Create text file for waypoint list as required by probtrackx2
WAYPOINT_TXT="${ROI_DIR}/waypoints.txt"
echo "$WAYPOINT" > "$WAYPOINT_TXT"

mkdir -p "$OUT_DIR"

# 2. Run probtrackx2
echo "[i] Tracking Left Corticospinal Tract (5000 samples per seed voxel)..."
probtrackx2 \
    -s "${BPX_DIR}/merged" \
    -m "$MASK" \
    -x "$SEED" \
    --waypoints="$WAYPOINT_TXT" \
    --avoid="$EXCLUDE" \
    --dir="$OUT_DIR" \
    -c 0.2 -S 2000 --steplength=0.5 -P 5000 \
    --opd --forcedir

# 3. Verify output
if [ -f "${OUT_DIR}/fdt_paths.nii.gz" ]; then
    WAYTOTAL=$(cat "${OUT_DIR}/waytotal")
    echo "[✓] Probabilistic tractography complete!"
    echo "[✓] Total valid streamlines generated: $WAYTOTAL"
else
    echo "ERROR: probtrackx2 output validation failed!"
    exit 1
fi

echo "=== [SUCCESS] Day 14 Probtrackx Execution Completed! ==="
