"""
Plots prevalences given a series of scenarios and model files (HDF5).
"""
import numpy as np


from _utils import (
    read_prevalences,
    comp_scaled_beta_posterior,
    floor_to_step,
    ceil_to_step,
    HIST_KWARGS,
)


def get_filename(modelname: str):
    return f"../data/{modelname}-prevalences.hdf5"


def plot_prevalences(
    models: dict,
    scenarios: dict,
    num_bins: int,
    color_cycle,
    hatch_cycle,
    fig,
    ax,
):
    data, min_value, max_value = read_prevalences(
        models=["base", *models.keys()],
        format_filename=get_filename,
        scenarios=scenarios.keys(),
        t_stages=["early", "late"],
    )
    min_value = floor_to_step(min_value, 2)
    max_value = ceil_to_step(max_value, 2)
    x = np.linspace(min_value, max_value, 200)
    bins = np.linspace(min_value, max_value, num_bins)

    for i, model in enumerate(models.keys()):
        for j, (scenario, label) in enumerate(scenarios.items()):
            base_hatch = next(hatch_cycle)
            color=next(color_cycle)
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

    return fig, ax
