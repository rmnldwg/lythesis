"""
Plot the auto-correlation times during a sampling run that continued until convergence.
"""
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lyscripts.plot.histograms import get_size

MODELS = {
    "add12": "I➜II",
    "add21": "II➜I",
}
COLORS = {
    "blue": '#005ea8',
    "green": '#00afa5',
    "orange": '#f17900',
    "red": '#ae0060',
    "gray": '#c5d5db',
}


if __name__ == "__main__":
    plt.style.use("../../../.mplstyle")

    fig, ax = plt.subplots(figsize=get_size())

    for name, label in MODELS.items():
        acor_times = pd.read_csv(f"../data/extended-{name}-v1-acor.csv")
        acor_times.plot(x="x", y="acor_times", ax=ax, label=label)

        xlim = ax.get_xlim()
        ax.set_xlim(
            left=max(xlim[0], acor_times["x"].values[0]),
            right=max(xlim[1], acor_times["x"].values[-1]),
        )

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x = np.linspace(*xlim, 10)
    ax.plot(x, x/30., "--", color="black", label="threshold")
    ax.set_xlabel("samples")
    ax.set_ylim(*ylim)
    ax.set_ylabel("auto-correlation estimate")
    ax.legend(loc="center right")

    plt.savefig(Path(__file__).with_suffix(".svg").name)
