import os
import subprocess

import numpy as np
import pandas as pd
from matplotlib.pyplot import colormaps
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "output.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_output(png_path, title):
    df = pd.read_csv(OUTPUT_PATH, header=None, sep=',', names=['X', 'Y'])
    projected = df[['X', 'Y']].to_numpy()

    scores = np.linalg.norm(projected, axis=1)
    scores_norm = (scores - np.min(scores)) / (np.max(scores) - np.min(scores))

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(projected[:, 0], projected[:, 1], s=8, c=colormaps["turbo"](scores_norm), alpha=0.3)
    ax.axis("off")
    ax.set_title(title, fontsize=30)

    plt.tight_layout()
    plt.savefig(png_path)
    plt.show()
    plt.close(fig)


results = []
tau = 1
d = 15
DATASETS = {
    "dataset2":"11 - m1_mechanically_imbalanced_electrically_50_ohm_fault_half_speed",
}


for windowSize in [150374]:#,102910,100000]:
        for label, fileName in DATASETS.items():
            subprocess.run(["./anomaly_detection.exe", str(d), str(tau), str(windowSize), str(fileName)])

            png_path = os.path.join(OUTPUT_DIR, f"output_{label}_d{d}_tau{tau}_w{windowSize}.png")
            plot_output(png_path, f"online-TDE")

print(results)
