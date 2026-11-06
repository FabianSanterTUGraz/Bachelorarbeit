import subprocess

import numpy as np
from matplotlib.pyplot import colormaps
from matplotlib import pyplot as plt

INPUT_NAME = "input"
d = 1200
W = 20480

def plot_embedding(ax, projected, title="TDE"):
    scores = np.linalg.norm(projected, axis=1)
    scores_norm = (scores - scores.min()) / (scores.max() - scores.min())
    ax.scatter(projected[:, 0], projected[:, 1], s=8, c=colormaps["turbo"](scores_norm),
               alpha=0.6, linewidths=0)
    limit = np.abs(projected).max() * 1.05
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    ax.set_title(title, fontsize=30)


subprocess.run(["./anomaly_detection", str(d), str(W), INPUT_NAME], check=True)

fingerprints = []
with open("output/output.txt") as file:
    for line in file:
        line = line.strip()
        if line == "---NEW-FINGERPRINT-START---":
            fingerprints.append([])
        elif line:
            fingerprints[-1].append([float(v) for v in line.split(",")])

for k, points in enumerate(fingerprints):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    plot_embedding(ax, np.array(points))
    #plt.savefig(f"results/tde_{k}.png")
    plt.show()
    plt.close(fig)