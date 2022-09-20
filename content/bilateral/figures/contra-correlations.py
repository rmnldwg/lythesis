"""
Plot historgams of the predicted prevalences for interesting scenarios w.r.t. the
connection from LNL III to V.
"""
from pathlib import Path
from itertools import cycle
import matplotlib.pyplot as plt

import numpy as np
import lyscripts.plot.histograms as lyhist

from _prevalences import plot_prevalences


MODELS = {
    "bilateral-v3": r"$\mathcal{M}_{ag}$",
    "midline-with-mixing-v3": r"$\mathcal{M}_\alpha$",
    "midline-without-mixing-v3": r"$\mathcal{M}_{full}$",
}
COLORS = {
    "blue": '#005ea8',
    "green": '#00afa5',
    # "orange": '#f17900',
    # "red": '#ae0060',
    # "gray": '#c5d5db',
}
HATCHES = [r"////", r"\\\\", r"...."]
COLOR_CYCLE = cycle(COLORS.values())
HATCH_CYCLE = cycle(HATCHES)
NBINS = 80
SCENARIOS = {
    "contraIIandIII/early/noext": ""
    "contraIIandIII/early/ext": ""
    "contraIIandIII/late/noext": ""
    "contraIIandIII/late/ext": ""
    "contraIInotIII/early/noext": ""
    "contraIInotIII/early/ext": ""
    "contraIInotIII/late/noext": ""
    "contraIInotIII/late/ext": ""
    "contraIIInotII/early/noext": ""
    "contraIIInotII/early/ext": ""
    "contraIIInotII/late/noext": ""
    "contraIIInotII/late/ext": ""
}


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))
    
    fig, ax = plt.subplots(
        nrows=len(MODELS), ncols=2,
        sharex="col", sharey="row",
        figsize=lyhist.get_size(width="full", ratio=2 * 1.6),
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
        ax[0,k].legend(fontsize=6.)

    ax[0,0].set_xlim(left=0., right=8.)

    for i, (model, model_label) in enumerate(MODELS.items()):
        ax[i,0].set_ylabel(model_label)
        ax[i,-1].set_ylim(bottom=0., top=1.5)

    plt.savefig(Path(__file__).with_suffix(".svg").name)
