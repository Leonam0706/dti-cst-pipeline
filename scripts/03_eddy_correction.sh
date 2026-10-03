set -e  # Exit on error

RAW_DIR="data/raw"
INPUT_DATA="${RAW_DIR}/data.nii.gz"
OUTPUT_DATA="${RAW_DIR}/data_eddy.nii.gz"
REF_VOL=0  # Use first volume (b=0) as registration target

echo "=== [DAY 7] Starting Motion & Eddy Current Correction ==="

# 1. Verify required raw dataset exists
if [ ! -f "$INPUT_DATA" ]; then
    echo "ERROR: Input dataset $INPUT_DATA not found!"
    exit 1
fi

# 2. Run FSL eddy_correct
echo "[i] Registering 4D volumes to reference volume index $REF_VOL..."
eddy_correct "$INPUT_DATA" "$OUTPUT_DATA" "$REF_VOL"

# 3. Verify eddy output creation
if [ -f "$OUTPUT_DATA" ]; then
    echo "[✓] Eddy current correction complete: $OUTPUT_DATA"
else
    echo "ERROR: Eddy correction failed!"
    exit 1
fi

echo "=== [SUCCESS] Day 7 Preprocessing Completed! ==="
