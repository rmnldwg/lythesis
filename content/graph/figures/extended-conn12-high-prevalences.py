"""
Plot historgams of the predicted prevalences for interesting high risk scenarios
w.r.t. the connection from LNL I to II or the other way around.
"""
from pathlib import Path
import matplotlib.pyplot as plt
from itertools import cycle

import numpy as np
import lyscripts.plot.histograms as lyhist

from _prevalences import plot_prevalences


MODELS = {
    "add12": "I➜II",
    "add21": "II➜I",
}
COLORS = {
    "red": '#ae0060',
    "orange": '#f17900',
    # "blue": '#005ea8',
    # "green": '#00afa5',
    # "gray": '#c5d5db',
}
HATCHES = [r"////", r"\\\\"]
COLOR_CYCLE = cycle(COLORS.values())
HATCH_CYCLE = cycle(HATCHES)
NBINS = 80
SCENARIOS = {
    "II": "LNL II overall",
    "IInotI": "LNL II without I",
}


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))
    
    fig, ax = plt.subplots(
        nrows=len(MODELS), ncols=2,
        sharex="col", sharey="row",
        figsize=lyhist.get_size(width="full", ratio=2.),
    )
    ax = np.reshape(ax, newshape=(len(MODELS), 2))

    fig, ax = plot_prevalences(
        models=MODELS,
        scenarios=SCENARIOS,
        num_bins=NBINS,
        color_cycle=COLOR_CYCLE,
        hatch_cycle=HATCH_CYCLE,
        fig=fig, ax=ax,
    )

    for k, stage in enumerate(["early", "late"]):
        ax[0,k].set_title(f"{stage} T-category")
        ax[-1,k].set_xlabel("prevalence [%]")
        ax[0,k].legend(fontsize=7.)

    for i, (model, model_label) in enumerate(MODELS.items()):
        ax[i,0].set_ylabel(model_label)

    plt.savefig(Path(__file__).with_suffix(".svg").name)
