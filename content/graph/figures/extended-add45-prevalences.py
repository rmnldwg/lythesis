"""
Plot historgams of the predicted prevalences for interesting scenarios w.r.t. the
connection from LNL III to V.
"""
from itertools import cycle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

import lyscripts.plot.histograms as lyhist

from utils import (
    read_prevalences,
    comp_scaled_beta_posterior,
    floor_to_step,
    ceil_to_step,
    HIST_KWARGS,
)


def get_filename(modelname: str):
    return f"../data/extended-{modelname}-v1-prevalences.hdf5"


MODELS = {
    "add45": "IV➜V",
}
COLORS = {
    "orange": '#f17900',
    "red": '#ae0060',
    "blue": '#005ea8',
    "green": '#00afa5',
    # "gray": '#c5d5db',
}
HATCHES = [r"////", r"\\\\", r"||||", r"----"]
COLOR_CYCLE = cycle(COLORS.values())
HATCH_CYCLE = cycle(HATCHES)
NBINS = 60
SCENARIOS = {
    # "IV": "LNL IV overall",
    # "V": "LNL V overall",
    "VandIV": "LNL V with IV",
    "VnotIV": "LNL V without IV",
}


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))

    fig, ax = plt.subplots(
        nrows=len(MODELS), ncols=2,
        sharex="col", sharey="row",
        figsize=lyhist.get_size(width="full", ratio=2 * 1.6),
    )
    ax = np.reshape(ax, newshape=(len(MODELS), 2))

    data, min_value, max_value = read_prevalences(
        models=["base", *MODELS.keys()],
        format_filename=get_filename,
        scenarios=SCENARIOS.keys(),
        t_stages=["early", "late"],
    )
    min_value = floor_to_step(min_value, 2)
    max_value = ceil_to_step(max_value, 2)
    x = np.linspace(min_value, max_value, 200)
    bins = np.linspace(min_value, max_value, NBINS)

    for i, model in enumerate(MODELS.keys()):
        for j, (scenario, label) in enumerate(SCENARIOS.items()):
            base_hatch = next(HATCH_CYCLE)
            color=next(COLOR_CYCLE)
            for k, stage in enumerate(["early", "late"]):
                num_success = data[model][scenario][stage]["num_success"]
                num_fail = data[model][scenario][stage]["num_fail"]
                posterior = comp_scaled_beta_posterior(x, num_success, num_fail)
                ax[i,k].hist(
                    data[model][scenario][stage]["values"],
                    label=label,
                    color=color,
                    zorder=2,
                    bins=bins,
                    **HIST_KWARGS,
                )
                ax[i,k].hist(
                    data["base"][scenario][stage]["values"],
                    label="base graph",
                    color="#97a3a7",
                    hatch=base_hatch,
                    zorder=1,
                    bins=bins,
                    histtype="step",
                    linewidth=1.5,
                    density=True,
                )
                ax[i,k].plot(
                    x, posterior,
                    label=f"{num_success} / {num_success + num_fail}",
                    color=color,
                    zorder=3,
                )
                ax[i,k].set_xlim(left=min_value, right=max_value)

    for k, stage in enumerate(["early", "late"]):
        ax[0,k].set_title(f"{stage} T-stage")
        ax[-1,k].set_xlabel("prevalence [%]")
        ax[0,k].legend(fontsize=7.)

    for i, (model, model_label) in enumerate(MODELS.items()):
        ax[i,0].set_ylabel(model_label)
        ax[i,0].set_ylim(bottom=0., top=1.5)

    plt.savefig("extended-add45-prevalences.svg")
