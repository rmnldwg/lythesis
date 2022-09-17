"""
Plot histograms comparing the predicted and observed prevalences for the models
based on the base graph, as well as the graphs adding connections from I to II and
from II to I respectively.
"""
from itertools import cycle
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import scipy.stats
import h5py

import lyscripts.plot.histograms as lyhist


def comp_scaled_beta_posterior(
    x: np.ndarray,
    num_success: int,
    num_total: int,
) -> np.ndarray:
    """
    Compute the Beta posterior over the success probability (in percent) for
    `num_success` observed successes and `num_total` tries.
    """
    num_fail = num_total - num_success
    return sp.stats.beta.pdf(x / 100., num_success+1, num_fail+1) / 100.


BASE_MODEL = Path("../data/extended-base-v1-prevalences.hdf5")
MODELS = {}
for tag in ["add12", "add21"]:
    MODELS[tag] = Path(f"../data/extended-{tag}-v1-prevalences.hdf5")


HIST_KWARGS = {
    "density": True,
    "histtype": "stepfilled",
    "alpha": 0.7,
}


if __name__ == "__main__":
    plt.style.use(Path("../../../.mplstyle"))

    # LOW RISK SCENARIOS
    COLORS = {
        "blue": '#005ea8',
        "green": '#00afa5',
        # "orange": '#f17900',
        # "red": '#ae0060',
        # "gray": '#c5d5db',
    }
    COLOR_CYCLE = cycle(COLORS.values())
    BINS = np.linspace(0., 16., 60)
    SCENARIOS = {
        "I": "LNL I overall",
        "InotII": "LNL I without II",
    }
    fig, ax = plt.subplots(
        nrows=2, ncols=2,
        sharex="col", sharey="row",
        figsize=lyhist.get_size(width="full", ratio=2.),
    )
    
    for i, (modelname, filepath) in enumerate(MODELS.items()):
        for scenario, label in SCENARIOS.items():
            color = next(COLOR_CYCLE)
            for j, stage in enumerate(["early", "late"]):
                with h5py.File(name=BASE_MODEL, mode="r") as h5_file:
                    base_dataset = h5_file[f"{scenario}/{stage}"]
                    base_values = base_dataset[:]
                with h5py.File(name=filepath, mode="r") as h5_file:
                    dataset = h5_file[f"{scenario}/{stage}"]
                    values = dataset[:]
                    posterior = comp_scaled_beta_posterior(
                        x=np.linspace(BINS[0], BINS[-1], 200),
                        num_success=dataset.attrs["num_match"],
                        num_total=dataset.attrs["num_total"]
                    )
                    
                    if scenario == "I":
                        hatches = "////"
                    else:
                        hatches = r"\\\\"

                    ax[i,j].hist(
                        100. * values,
                        label=label,
                        color=color,
                        zorder=2,
                        bins=BINS,
                        **HIST_KWARGS,
                    )
                    ax[i,j].hist(
                        100. * base_values,
                        label="base graph",
                        color='#97a3a7',
                        hatch=hatches,
                        bins=BINS,
                        density=True,
                        histtype="step",
                        linewidth=1.5,
                        zorder=1,
                    )                    
                    ax[i,j].plot(
                        np.linspace(BINS[0], BINS[-1], 200), posterior,
                        label=f"{int(dataset.attrs['num_match'])} / {int(dataset.attrs['num_total'])}",
                        color=color,
                        zorder=3,
                    )
                    # ax[i,j].set_xlim(BINS[0], BINS[-1])
                    ax[i,j].set_ylim(0., 1.5)
                    ax[i,j].set_yticks([0., 0.5, 1., 1.5])
                    
                    if stage == "early":
                        if i == 0:
                            ax[i,j].legend()
                            ax[i,j].set_title("early T-stage")
                        else:
                            ax[i,j].set_xlabel("prevalence [%]")
                        ax[i,j].set_xlim(0., 10.)
                    else:
                        if i == 0:
                            ax[i,j].legend()
                            ax[i,j].set_title("late T-stage")
                        else:
                            ax[i,j].set_xlabel("prevalence [%]")
                        ax[i,j].set_xlim(0., 16.)
    
    plt.savefig("extended-connection12-low-prevalences.png")

    # HIGH RISK SCENARIOS
    COLORS = {
        "orange": '#f17900',
        "red": '#ae0060',
        # "blue": '#005ea8',
        # "green": '#00afa5',
        # "gray": '#c5d5db',
    }
    COLOR_CYCLE = cycle(COLORS.values())
    BINS = np.linspace(50., 100., 100)
    SCENARIOS = {
        "IInotI": "LNL II without I",
        "II": "LNL II overall",
    }
    fig, ax = plt.subplots(
        nrows=2, ncols=2,
        sharex="col", sharey="row",
        figsize=lyhist.get_size(width="full", ratio=2.),
    )
    
    for i, (modelname, filepath) in enumerate(MODELS.items()):
        for scenario, label in SCENARIOS.items():
            color = next(COLOR_CYCLE)
            for j, stage in enumerate(["early", "late"]):
                with h5py.File(name=BASE_MODEL, mode="r") as h5_file:
                    base_dataset = h5_file[f"{scenario}/{stage}"]
                    base_values = base_dataset[:]
                with h5py.File(name=filepath, mode="r") as h5_file:
                    dataset = h5_file[f"{scenario}/{stage}"]
                    values = dataset[:]
                    posterior = comp_scaled_beta_posterior(
                        x=np.linspace(BINS[0], BINS[-1], 200),
                        num_success=dataset.attrs["num_match"],
                        num_total=dataset.attrs["num_total"]
                    )
                    
                    if scenario == "IInotI":
                        hatches = "////"
                    else:
                        hatches = r"\\\\"

                    ax[i,j].hist(
                        100. * values,
                        label=label,
                        color=color,
                        zorder=2,
                        bins=BINS,
                        **HIST_KWARGS,
                    )
                    ax[i,j].hist(
                        100. * base_values,
                        label="base graph",
                        color='#97a3a7',
                        hatch=hatches,
                        bins=BINS,
                        density=True,
                        histtype="step",
                        linewidth=1.5,
                        zorder=1,
                    )                    
                    ax[i,j].plot(
                        np.linspace(BINS[0], BINS[-1], 200), posterior,
                        label=f"{int(dataset.attrs['num_match'])} / {int(dataset.attrs['num_total'])}",
                        color=color,
                        zorder=3,
                    )
                    # ax[i,j].set_xlim(BINS[0], BINS[-1])
                    # ax[i,j].set_ylim(0., 1.5)
                    # ax[i,j].set_yticks([0., 0.5, 1., 1.5])
                    
                    if stage == "early":
                        if i == 0:
                            ax[i,j].legend()
                            ax[i,j].set_title("early T-stage")
                        else:
                            ax[i,j].set_xlabel("prevalence [%]")
                        ax[i,j].set_xlim(55., 75.)
                    else:
                        if i == 0:
                            ax[i,j].legend()
                            ax[i,j].set_title("late T-stage")
                        else:
                            ax[i,j].set_xlabel("prevalence [%]")
                        ax[i,j].set_xlim(65., 85.)
    
    plt.savefig("extended-connection12-high-prevalences.png")