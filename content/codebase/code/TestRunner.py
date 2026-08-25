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
    df = pd.read_csv(OUTPUT_PATH, nrows=151017, header=None, sep=',', names=['X', 'Y'])
    projected = df[['X', 'Y']].to_numpy()

    scores = np.linalg.norm(projected, axis=1)

    inner_cutoff = np.percentile(scores, 50)
    keep = scores >= inner_cutoff
    projected = projected[keep]
    scores = scores[keep]

    scores_norm = (scores - np.min(scores)) / (np.max(scores) - np.min(scores))

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(projected[:, 0], projected[:, 1], s=8, c=colormaps["turbo"](scores_norm), alpha=0.3)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(True, alpha=0.3)
    ax.set_title(title, fontsize=30)

    plt.show()


results = []
tau = 1
DATASETS = {
    "healthy(1)": "01 - m1_half_shaft_speed_no_mechanical_load",
    "healty(2)":  "02 - m1_load_0.5Nm_half_speed",
    "faulty1":"19 - m1_mechanically_imbalanced_load_0.5Nm_m2_mechanically_imbalanced_on_background_half_speed",
    "faulty1.5":"26 - m1_mechanically_umbalanced_electrically_50_ohm_fault_load_0.5Nm_m2_umbalanced_on_background_half_speed",
    "faulty2" : "30 - m1_mechanically_imbalanced_electrically_150_ohm_fault_m2_imbalanced_on_background_rotated_half_speed",
}

for windowSize in [1200,1500]:#,15000,100000]:
    for d in [20]:
        for label, fileName in DATASETS.items():
            subprocess.run(["./anomaly_detection.exe", str(d), str(tau), str(windowSize), str(fileName)])

            png_path = os.path.join(OUTPUT_DIR, f"output_{label}_d{d}_tau{tau}_w{windowSize}.png")
            plot_output(png_path, f"TDE {label} d={d} tau={tau} w={windowSize}")

print(results)
