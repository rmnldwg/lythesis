"""
Plot the auto-correlation times during a sampling run that continued until convergence.
"""
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from lyscripts.plot.histograms import get_size

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

    acor_times = pd.read_csv(f"../data/complete-v1-acor.csv")
    acor_times.plot(x="x", y="acor_times", ax=ax, legend=False)

    xlim = ax.get_xlim()
    ax.set_xlim(left=0., right=max(xlim[1], acor_times["x"].values[-1]))

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x = np.linspace(*xlim, 10)
    ax.plot(x, x/30., "--", color="black", label="threshold")
    ax.set_xlabel("samples $N$")
    ax.set_ylim(*ylim)
    ax.set_ylabel(r"auto-correlation estimate $\hat{\tau}$")

    plt.savefig(Path(__file__).with_suffix(".svg").name)
