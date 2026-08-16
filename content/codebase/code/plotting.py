import os
import numpy as np
import pandas as pd
from matplotlib.pyplot import colormaps
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "output.txt")
PNG_PATH = os.path.join(OUTPUT_DIR, "output.png")

df = pd.read_csv(OUTPUT_PATH, nrows=111563, header=None, sep=',', names=['X', 'Y'])

projected = df[['X', 'Y']].to_numpy()

scores = np.linalg.norm(projected, axis=1)
scores_norm = (scores - np.min(scores)) / (np.max(scores) - np.min(scores))

fig, ax = plt.subplots(figsize=(7, 7))

ax.scatter(projected[:, 0], projected[:, 1], s=8, c=colormaps["turbo"](scores_norm))
ax.axis("off")
ax.set_title("TDE", fontsize=30)

plt.savefig(PNG_PATH)
plt.show()