set -e  # Exit on error

RAW_DIR="data/raw"
DATA="${RAW_DIR}/data.nii.gz"
B0_VOL="${RAW_DIR}/nodif.nii.gz"
B0_BRAIN="${RAW_DIR}/nodif_brain.nii.gz"
B0_MASK="${RAW_DIR}/nodif_brain_mask.nii.gz"

echo "=== [DAY 6] Starting Brain Extraction (BET) ==="

# 1. Verify raw input exists
if [ ! -f "$DATA" ]; then
    echo "ERROR: Raw file $DATA not found!"
    exit 1
fi

# 2. Extract first b=0 volume (volume index 0, length 1)
echo "[i] Extracting baseline b=0 volume..."
fslroi "$DATA" "$B0_VOL" 0 1

# 3. Run FSL BET with fractional intensity threshold f=0.25 and output mask (-m)
echo "[i] Running FSL BET on b=0 volume..."
bet "$B0_VOL" "$B0_BRAIN" -m -f 0.25

# 4. Verify mask output
if [ -f "$B0_MASK" ]; then
    echo "[✓] Brain mask successfully created: $B0_MASK"
else
    echo "ERROR: Brain mask creation failed!"
    exit 1
fi

echo "=== [SUCCESS] Brain Extraction Completed! ==="
