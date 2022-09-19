"""
Plot historgams of the predicted prevalences for interesting low risk scenarios
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
    "blue": '#005ea8',
    "green": '#00afa5',
    # "orange": '#f17900',
    # "red": '#ae0060',
    # "gray": '#c5d5db',
}
HATCHES = [r"////", r"\\\\"]
COLOR_CYCLE = cycle(COLORS.values())
HATCH_CYCLE = cycle(HATCHES)
NBINS = 80
SCENARIOS = {
    "I": "LNL I overall",
    "InotII": "LNL I without II",
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
        ax[0,k].set_title(f"{stage} T-stage")
        ax[-1,k].set_xlabel("prevalence [%]")
        ax[0,k].legend(fontsize=7.)

    ax[-1,0].set_xlim(left=0., right=12.)

    for i, (model, model_label) in enumerate(MODELS.items()):
        ax[i,0].set_ylabel(model_label)
        ax[i,0].set_ylim(bottom=0., top=1.5)

    plt.savefig(Path(__file__).with_suffix(".svg").name)
