import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

# Paths
data_path = 'data/raw/data.nii.gz'
output_png = 'data/raw/qa_b0_overview.png'

if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit(1)

# Load 4D diffusion volume
img = nib.load(data_path)
data = img.get_fdata()

# Extract b=0 volume (first 3D volume)
b0_vol = data[:, :, :, 0]

# Calculate middle indices
x_mid, y_mid, z_mid = [dim // 2 for dim in b0_vol.shape]

# Render orthogonal slices
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
fig.suptitle('Day 5 Baseline Visual QA - $b=0$ Volume', fontsize=14)

axes[0].imshow(np.rot90(b0_vol[x_mid, :, :]), cmap='gray')
axes[0].set_title(f'Sagittal (Slice {x_mid})')
axes[0].axis('off')

axes[1].imshow(np.rot90(b0_vol[:, y_mid, :]), cmap='gray')
axes[1].set_title(f'Coronal (Slice {y_mid})')
axes[1].axis('off')

axes[2].imshow(np.rot90(b0_vol[:, :, z_mid]), cmap='gray')
axes[2].set_title(f'Axial (Slice {z_mid})')
axes[2].axis('off')

plt.tight_layout()
plt.savefig(output_png, dpi=150)
print(f"[✓] Visual QA image generated and saved to: {output_png}")
