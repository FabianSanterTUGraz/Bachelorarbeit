# Required Python libraries:
 #-numpy
 #-matplotlib
 # Install via: pip3 install numpy matplotlib

import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.pyplot import colormaps

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "code", "output", "output.txt")
BENCHMARK_RESULTS_PATH = os.path.join(SCRIPT_DIR, "data", "benchmarkResults.txt")
COMPARISON_PLOT_PATH = os.path.join(SCRIPT_DIR, "data", "StaticVsDynamic.png")


def plot_scatter(ax, points, title):
    scores = np.linalg.norm(points, axis=1)
    scores_norm = (scores - np.min(scores)) / (np.max(scores) - np.min(scores))
    ax.scatter(points[:, 0], points[:, 1], s=8, c=colormaps["turbo"](scores_norm), alpha=0.3)
    ax.axis("off")
    ax.set_title(title, fontsize=16)


def main(output_path=OUTPUT_PATH, benchmark_path=BENCHMARK_RESULTS_PATH, plot_path=COMPARISON_PLOT_PATH):
    dynamic = np.loadtxt(output_path, delimiter=",")
    static = np.loadtxt(benchmark_path, delimiter=",")

    rows = min(len(dynamic), len(static))
    dynamic = dynamic[:rows].copy()
    static = static[:rows]

    # PCA axes are only defined up to sign: align the streaming result's sign
    # to the batch reference before plotting/comparing (see computeDelta.py).
    sign = np.sign(np.sum(dynamic * static, axis=0))
    sign[sign == 0] = 1
    dynamic *= sign

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    plot_scatter(axes[0], static, "static (batch PCA)")
    plot_scatter(axes[1], dynamic, "dynamic (incremental)")

    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close(fig)
    print(f"Saved comparison plot to: {plot_path}")


if __name__ == "__main__":
    main()
